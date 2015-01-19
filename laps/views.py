from laps.models import ConfigurationAttribute, Lap, Machine, MachineConfiguration, Race, Racer, Track
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import DetailView
from braces.views import JSONResponseMixin

from django.contrib.auth.decorators import login_required

import forms, util

class RacesByYear:
	races=None
	years=None
	dates=None

	def get_races(self, race_filter_q=Q()):
		self.races = Race.objects.filter(race_filter_q).order_by('date')
		self.years = []
		self.dates = []
		race_by_date={}
		for race in self.races:
			year = race.date.year
			if not(year in self.years):
				self.years.append(year)
			if not(race.date in self.dates):
				self.dates.append(race.date)


def races(request):
	races = RacesByYear()
	races.get_races()
	return render(request, 'laps/races.html', {
		'races':races.races,
		'years':races.years,
		'dates':races.dates })

def race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	template_dict = { 'race': race }
	if request.user.is_authenticated():
		template_dict['add_config_attr_form'] = forms.AddConfigurationAttributeToRaceForm()
	return render(request, 'laps/race.html', template_dict)

@login_required
def add_config_attr_to_race(request, race_id):
	race = Race.objects.get(id=race_id)
	if request.method == 'POST':
		form = forms.AddConfigurationAttributeToRaceForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				key = form.cleaned_data['key']
				value = form.cleaned_data['value']
				attr, created = ConfigurationAttribute.objects.get_or_create(key=key, value=value)
				attr.machine_configurations.add(race.machine_config)
				attr.save()
	return HttpResponseRedirect("/laps/races/%d" % race.id)

def machine(request, machine_id):
	machine = get_object_or_404(Machine, pk=machine_id)
	races = RacesByYear()
	races.get_races(Q(machine_config__machine=machine))
	return render(request, 'laps/machine.html', {
		'machine': machine,
		'races':races.races,
		'years':races.years,
		'dates':races.dates})

def machines(request):
	machines = Machine.objects.all()
	return render(request, 'laps/machines.html', {'machines': machines })

def tracks(request):
	tracks = Track.objects.all()
	return render(request, 'laps/tracks.html', {'tracks': tracks })

def track(request, track_id):
	track = get_object_or_404(Track, pk=track_id)
	races = RacesByYear()
	races.get_races(Q(track__id=track_id))
	return render(request, 'laps/track.html', {
		'track': track,
		'races':races.races,
		'years':races.years,
		'dates':races.dates})

def index(request):
	return render(request, 'laps/index.html', {})

class LapTrendAJAXView(JSONResponseMixin, DetailView):
	model = Track
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		track_id = kwargs['track_id']
		track = Track.objects.get(pk=track_id)
		races = Race.objects.filter(track=track).order_by('date')
		result = {
			u'best': [],
			u'avg': [],
			u'race': [],
		}
		for race in races:
			result['best'].append(race.best_lap_time())
			result['avg'].append(race.average_lap_time())
			result['race'].append({
				u'date': race.date,
				u'name': race.name,
				u'id': race.id
				})

		return self.render_json_response(result)

class LapsAJAXView(JSONResponseMixin, DetailView):
	model = Race
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		race_id = kwargs['race_id']
		race = Race.objects.get(pk=race_id)
		result = []
		for lap in race.laps.values('num', 'time'):
			result.append({u'num': lap['num'], u'time': lap['time']})

		return self.render_json_response(result)

class TracksRacedAJAXView(JSONResponseMixin, DetailView):
	model = Race
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		machine_id = kwargs['machine_id']
		machine = Machine.objects.get(pk=machine_id)
		result = []
		for track in Track.objects.all().order_by('name'):
			num_races = Race.objects.filter(track=track, machine_config__machine=machine).count()
			if not(num_races == 0):
				result_item = {
						u'track': {
							u'id': track.id,
							u'name': track.name
						},
						u'num_races': num_races
					}
				result.append(result_item)

		return self.render_json_response(result)

# TODO: allow more than one racer! synonymous with user?
def current_racers_bike(name):
	return Machine.objects.get(name=name)

@login_required
def create_race(request):
	if request.method == 'POST':
		form = forms.EditRaceForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				machine = current_racers_bike(form.cleaned_data['machine_name'])
				config = machine.empty_configuration()

				race = Race()
				race.name = form.cleaned_data['name']
				race.date = form.cleaned_data['date']
				race.track = Track.objects.get(name=form.cleaned_data['track_name'])
				race.num_laps = form.cleaned_data['num_laps']
				race.machine_config = config
				race.save()
				return HttpResponseRedirect("/laps/races/%d/edit/laps" % race.id)
	else:
		# TODO: initial values (date=today, )
		#initial_form_values = race.__dict__
		#form = forms.EditRaceForm(initial_form_values)
		form = forms.EditRaceForm()
	return render(request, 'laps/new_race.html', { 'form':form })

@login_required
def edit_race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	if request.method == 'POST':
		form = forms.EditRaceForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				race.name = form.cleaned_data['name']
				race.date = form.cleaned_data['date']
				race.track = Track.objects.get(name=form.cleaned_data['track_name'])
				race.num_laps = form.cleaned_data['num_laps']
				if not(race.machine_config.machine.name == form.cleaned_data['name']):
					# The machine was changed
					machine = current_racers_bike(form.cleaned_data['machine_name'])
					race.machine_config = machine.empty_configuration()
				race.save()
				return HttpResponseRedirect("/laps/races/%d/edit/laps" % race.id)
	else:
		initial_form_values = race.__dict__
		initial_form_values['machine_name'] = race.machine_config.machine.name
		initial_form_values['track_name'] = race.track.name 
		form = forms.EditRaceForm(initial_form_values)
	return render(request, 'laps/edit_race.html', { 'form':form, 'race':race })

# TODO: allow more than one racer! synonymous with user?
def current_racer():
	return Racer.objects.all()[0]

@login_required
def edit_race_laps(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	laps = Lap.objects.filter(race__id=race_id)
	if race.num_laps == 0:
		# No laps to enter/edit, so just return to the race page
		return HttpResponseRedirect("/laps/races/%d" % race.id)

	if request.method == 'POST':
		# TODO: include notification to say update was successful
		form = forms.EditLapsForm(request.POST, num_laps=race.num_laps, laps=laps)
		if form.is_valid():
			lap_dict = form.get_lap_dict()
			for lap_num in xrange(1, form.num_laps + 1):
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
						lap, created = Lap.objects.get_or_create(race=race, num=lap_num, time=lap_time_s, racer=current_racer())
					lap.save()
		else:
			raise Exception('Invalid form submission')
		return HttpResponseRedirect("/laps/races/%d" % race.id)
	else:
		form = forms.EditLapsForm(num_laps=race.num_laps, laps=laps)
	return render(request, 'laps/edit_laps.html', { 'form':form, 'race':race })


