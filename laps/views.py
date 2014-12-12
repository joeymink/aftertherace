from laps.models import Machine, Race, Track
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import DetailView
from braces.views import JSONResponseMixin

from django.contrib.auth.decorators import login_required

import forms

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
	return render(request, 'laps/race.html', {'race': race })

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


@login_required
def edit_race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	if request.method == 'POST':
		form = forms.EditRaceForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				race.name = form.cleaned_data['name']
				race.save()
				return HttpResponseRedirect("/laps/races/%d" % race.id)
	else:
		form = forms.EditRaceForm(race.__dict__)
	return render(request, 'laps/edit_race.html', { 'form':form, 'race':race })


