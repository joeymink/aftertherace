from laps.models import ConfigurationAttribute, Lap, Machine, MachineConfiguration, Race, Track
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import DetailView
from braces.views import JSONResponseMixin

from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from laps import forms, util
from laps.views.user_util import assert_user_logged_in

import datetime

@login_required
def logout(request):
	return auth_views.logout(request, template_name='laps/logout.html')

class AugmentedUser:
	def __init__(self, user):
		self.user = user

	def races(self):
		return Race.objects.filter(user=self.user).order_by('date_time')

	def first_race(self):
		try:
			return Lap.objects.filter(race__user=self.user).order_by('race__date_time')[0].race
		except IndexError:
			return None

	def last_race(self):
		laps = Lap.objects.filter(race__user=self.user).order_by('-race__date_time')
		if laps.count() > 0:
			return laps[0].race
		return None

	def num_laps(self):
		return Lap.objects.filter(race__user=self.user).count()

	def tracks(self):
		return Track.objects.filter(races__user=self.user).order_by('name').distinct()

	def fastest_races(self):
		races = []
		for track in self.tracks():
			fastest_race = None
			for race in Race.objects.filter(user=self.user, track=track):
				if race.best_lap_time() is None:
					continue
				if fastest_race is None:
					fastest_race = race
				elif race.best_lap_time() < fastest_race.best_lap_time():
					fastest_race = race
			races.append(fastest_race)
		return races

def racer(request, username):
	user = get_user_model().objects.get(username=username)
	return render(request, 'laps/racer.html', {
		'racer':user.username,
		'auguser':AugmentedUser(user)})

@login_required
def profile(request):
	return racer(request, request.user.username)

class RacesByYear:
	races=None
	years=None
	dates=None

	def get_races(self, race_filter_q=Q()):
		self.races = Race.objects.filter(race_filter_q).order_by('date_time')
		self.years = []
		self.dates = []
		race_by_date={}
		for race in self.races:
			year = race.date_time.year
			if not(year in self.years):
				self.years.append(year)
			if not(race.date_time.date() in self.dates):
				self.dates.append(race.date_time.date())

def tracks(request, username):
	user = get_object_or_404(get_user_model(), username=username)
	tracks = Track.objects.filter(races__user=user).distinct()
	return render(request, 'laps/tracks.html', {
		'racer':user.username,
		'tracks': tracks })

def track(request, username, track_id):
	user = get_object_or_404(get_user_model(), username=username)
	track = get_object_or_404(Track, pk=track_id)
	races = RacesByYear()
	races.get_races(Q(track__id=track_id))
	return render(request, 'laps/track.html', {
		'racer': user.username,
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
		username = kwargs['username']
		track_id = kwargs['track_id']

		user = get_object_or_404(get_user_model(), username=username)
		track = get_object_or_404(Track, pk=track_id)
		races = Race.objects.filter(track=track, user=user).order_by('date_time')
		result = {
			u'best': [],
			u'avg': [],
			u'race': [],
		}
		for race in races:
			if race.laps.count() > 0:
				result['best'].append(race.best_lap_time())
				result['avg'].append(race.average_lap_time())
				result['race'].append({
					u'date': race.date_time,
					u'name': race.name,
					u'id': race.id
					})

		return self.render_json_response(result)

class LapsAJAXView(JSONResponseMixin, DetailView):
	model = Race
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		username = kwargs['username']
		race_id = kwargs['race_id']

		user = get_object_or_404(get_user_model(), username=username)
		race = get_object_or_404(Race, pk=race_id, user=user)
		result = []
		for lap in race.laps.values('num', 'time').order_by('num'):
			result.append({u'num': lap['num'], u'time': lap['time']})

		return self.render_json_response(result)

class TracksRacedAJAXView(JSONResponseMixin, DetailView):
	model = Race
	json_dumps_kwargs = {u"indent": 2}

	def get(self, request, *args, **kwargs):
		username = kwargs['username']
		machine_id = kwargs['machine_id']
		
		user = get_object_or_404(get_user_model(), username=username)
		machine = get_object_or_404(Machine, pk=machine_id, user=user)
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


