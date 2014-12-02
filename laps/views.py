from laps.models import Machine, Race, Track
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.views.generic import DetailView
from braces.views import JSONResponseMixin

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

def chart_test(request):
	return render(request, 'laps/chart_test.html', {})


class LapTrendAJAXView(JSONResponseMixin, DetailView):
	model = Track
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		track = Track.objects.filter(name='NJMP - Thunderbolt')[0]
		races = Race.objects.filter(track=track).order_by('date')
		result = {
			u'best': [],
			u'avg': [],
			u'date': [],
		}
		for race in races:
			result['best'].append(race.best_lap_time())
			result['avg'].append(race.average_lap_time())
			result['date'].append(race.date)

		return self.render_json_response(result)


