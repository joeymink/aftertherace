from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.urlresolvers import reverse

from laps.models import ConfigurationAttribute, Lap, Machine, MachineConfiguration, Race, Track
from laps.views import RacesByYear
from laps.views.user_util import assert_user_logged_in
from laps import forms, lapimport, util

def races(request, username):
	user = get_user_model().objects.get(username=username)
	races = RacesByYear()
	races.get_races(Q(user=user))
	return render(request, 'laps/races.html', {
		'racer':user.username,
		'races':races.races,
		'years':races.years,
		'dates':races.dates })

def race(request, username, race_id):
	user = get_object_or_404(get_user_model(), username=username)
	race = get_object_or_404(Race, pk=race_id, user=user)
	template_dict = {
		'racer': user.username,
		'race': race }
	if request.user.is_authenticated():
		template_dict['add_config_attr_form'] = forms.AddConfigurationAttributeToRaceForm()
	return render(request, 'laps/race.html', template_dict)

@login_required
def add_config_attr_to_race(request, username, race_id):
	user = assert_user_logged_in(username, request)
	race = get_object_or_404(Race, pk=race_id)
	if not(race.user == user):
		raise PermissionDenied

	if request.method == 'POST':
		form = forms.AddConfigurationAttributeToRaceForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				key = form.cleaned_data['key']
				value = form.cleaned_data['value']
				attr, created = ConfigurationAttribute.objects.get_or_create(key=key, value=value)
				attr.machine_configurations.add(race.machine_config)
				attr.save()
	return HttpResponseRedirect(reverse('laps:race', args=(username, race.id)))

@login_required
def create_race(request, username):
	user = assert_user_logged_in(username, request)
	if request.method == 'POST':
		form = forms.EditRaceForm(request.POST, user=user)
		if form.has_changed():
			if form.is_valid():
				machine = Machine.objects.get(name=form.cleaned_data['machine_name'], user=user)
				config = machine.empty_configuration()

				race = Race()
				race.name = form.cleaned_data['name']
				race.date_time = form.cleaned_data['date_time']
				race.track = Track.objects.get(name=form.cleaned_data['track_name'])
				race.num_laps = form.cleaned_data['num_laps']
				race.organization = form.cleaned_data['organization']
				race.machine_config = config
				race.user = user
				# If user hits back & returns to new race form,
				# help them out by not creating a race twice or
				# failing on uniqueness constraint:
				race, created = Race.objects.get_or_create(
					name=race.name, date_time=race.date_time, track=race.track,
					num_laps=race.num_laps, organization=race.organization,
					machine_config=race.machine_config, user=race.user)
				return HttpResponseRedirect(reverse('laps:edit_race_laps', args=(username, race.id)))
	else:
		form = forms.EditRaceForm(user=user)
	return render(request, 'laps/new_race.html', { 'form':form, 'racer': user.username })

@login_required
def import_race(request, username):
	user = assert_user_logged_in(username, request)
	if request.method == 'POST':
		form = forms.ImportMotolaptimesForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				motolaptimes_url = form.cleaned_data['url']
				parsed_content = lapimport.extract_from_motolaptimes(motolaptimes_url)
				race = lapimport.motolaptimes_as_model(parsed_content, user)
				return HttpResponseRedirect(reverse('laps:race', args=(user.username, race.id)))
	else:
		form = forms.ImportMotolaptimesForm()
	return render(request, 'laps/import_race.html', { 'form':form, 'racer': user.username })

@login_required
def edit_race(request, username, race_id):
	user = assert_user_logged_in(username, request)
	race = get_object_or_404(Race, pk=race_id)
	if not(race.user == user):
		raise PermissionDenied

	if request.method == 'POST':
		form = forms.EditRaceForm(request.POST, user=user)
		if form.has_changed():
			if form.is_valid():
				race.name = form.cleaned_data['name']
				race.date_time = form.cleaned_data['date_time']
				race.track = Track.objects.get(name=form.cleaned_data['track_name'])
				race.num_laps = form.cleaned_data['num_laps']
				race.organization = form.cleaned_data['organization']
				if (race.machine_config is None) or not(race.machine_config.machine.name == form.cleaned_data['machine_name']):
					# The machine was changed
					machine = Machine.objects.get(name=form.cleaned_data['machine_name'], user=user)
					race.machine_config = machine.empty_configuration()
				race.save()
				return HttpResponseRedirect(reverse('laps:edit_race_laps', args=(username, race.id)))
	else:
		initial_form_values = race.__dict__
		if race.machine_config:
			initial_form_values['machine_name'] = race.machine_config.machine.name
		if race.track:
			initial_form_values['track_name'] = race.track.name
		initial_form_values['num_laps'] = race.num_laps
		form = forms.EditRaceForm(initial_form_values, user=user)
	return render(request, 'laps/edit_race.html', { 'form':form, 'race':race, 'racer': username })

@login_required
def edit_race_laps(request, username, race_id):
	user = assert_user_logged_in(username, request)
	race = get_object_or_404(Race, pk=race_id)
	if not(race.user == user):
		raise PermissionDenied

	laps = Lap.objects.filter(race__id=race_id)
	if race.num_laps == 0:
		# No laps to enter/edit, so just return to the race page
		return HttpResponseRedirect(reverse('laps:race', args=(username, race.id)))

	if request.method == 'POST':
		# TODO: include notification to say update was successful
		form = forms.EditLapsForm(request.POST, num_laps=race.num_laps, laps=laps)
		if form.is_valid():
			lap_dict = form.get_lap_dict()
			for lap_num in xrange(1, form.num_laps + 1): # TODO: Maybe delete all laps and recreate?
				if not(lap_num in lap_dict) or not(lap_dict[lap_num]):	# no lap time given
					try:
						lap = Lap.objects.get(race=race, num=lap_num)
						lap.delete()
					except Lap.DoesNotExist:
						pass	# Lap doesn't exist? No problem
				else:	# lap time given for this lap number
					lap_time_s = util.interpret_time(lap_dict[lap_num])
					try:
						lap = Lap.objects.get(race=race, num=lap_num)
						# Update exist lap:
						lap.time = lap_time_s
					except Lap.DoesNotExist:
						# Create a new lap:
						lap, created = Lap.objects.get_or_create(race=race, num=lap_num, time=lap_time_s)
					except Lap.MultipleObjectsReturned:
						# TODO: had an issue with race that had same lap number twice...
						# TODO: maybe ensure uniqueness here?
						Lap.objects.filter(race=race, num=lap_num).delete()
						lap, created = Lap.objects.get_or_create(race=race, num=lap_num, time=lap_time_s)
					lap.save()
			return HttpResponseRedirect(reverse('laps:race', args=(username, race.id)))
	else:
		form = forms.EditLapsForm(num_laps=race.num_laps, laps=laps)
	return render(request, 'laps/edit_laps.html', { 'form':form, 'race':race, 'racer':user.username })