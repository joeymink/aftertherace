from django.db import models
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

# Machine

class Machine(models.Model):
	name = models.CharField(max_length=100, unique=True)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __unicode__(self):
		return self.name

	def num_laps(self):
		return Lap.objects.filter(race__machine_config__machine=self).count()

	def races(self):
		return Race.objects.filter(machine_config__machine=self).order_by('date_time')

	def first_race(self):
		try:
			return Lap.objects.filter(race__machine_config__machine=self).order_by('race__date_time')[0].race
		except IndexError:
			return None

	def last_race(self):
		return Lap.objects.filter(race__machine_config__machine=self).order_by('-race__date_time')[0].race

	def unique_configuration_keys(self):
		keys = []
		for c in self.configurations.all():
			for key in ConfigurationAttribute.objects.filter(machine_configurations__in=[c.id]).order_by('key').values('key').distinct():
				if not(key in keys):
					keys.append(key)
		return keys

	def empty_configuration(self):
		""" Return the empty configuration for this machine """
		for c in self.configurations.all():
			if len(c.attributes.values()) == 0:
				return c
		new_config = MachineConfiguration(machine=self)
		new_config.save()
		return new_config

	def unique_configurations(self):
		# find unique machine configurations:
		config_dict = {}
		config_list = []
		for c in self.configurations.all():
			attrs = ConfigurationAttribute.objects.filter(machine_configurations__in=[c.id]).order_by('key')
			unique_key = ""
			for a in attrs:
				unique_key="%s%s%s" % (unique_key, a.key, a.value)
			if not(unique_key in config_dict):
				config_dict[unique_key] = ""
				config_list.append(attrs)
		return config_list

	def events_by_organization(self):
		return_dict = {}
		races = self.races()
		for race in races:
			if not(race.organization in return_dict):
				return_dict[race.organization] = []
			if not(race.name in return_dict[race.organization]):
				return_dict[race.organization].append(race.name)
		return return_dict

	def tracks(self):
		return Track.objects.filter(races__machine_config__machine=self).order_by('name').distinct()

class MachineConfiguration(models.Model):
	name = models.CharField(max_length=100)
	machine = models.ForeignKey(Machine, related_name='configurations')
	def __unicode__(self):
		return "%s (%s)" % (self.name, self. machine.name)

class ConfigurationAttribute(models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	machine_configurations = models.ManyToManyField(MachineConfiguration, related_name='attributes')
	def __unicode__(self):
		return "%s: %s" % (self.key, self.value)
	
	class Meta:
		unique_together = ('key', 'value')

# Track

class Track(models.Model):
	name=models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return self.name

	def machines(self, user):
		return Machine.objects.filter(configurations__races__track=self, user=user).distinct()

	def races(self):
		return Race.objects.filter(track=self)

	def laps(self):
		return Lap.objects.filter(race__track=self)

# Racer

class Racer(models.Model):
	# TODO: does this model even need to exist anymore?
	first = models.CharField(max_length=100)
	last = models.CharField(max_length=100)
	middle = models.CharField(max_length=100)
	dob = models.DateTimeField(null=True)
	def __unicode__(self):
		return ' '.join([self.first, self.middle, self.last])

# Race

class Race(models.Model):
	name = models.CharField(max_length=100)
	machine_config = models.ForeignKey(MachineConfiguration, blank=True, null=True, related_name='races')
	date_time = models.DateTimeField()
	track = models.ForeignKey(Track, related_name="races", null=True)
	organization = models.CharField(max_length=100)
	conditions = models.CharField(max_length=100)
	num_laps = models.IntegerField(default=0)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	is_team = models.BooleanField(default=False)

	def __unicode__(self):
		if not(self.track is None):
			trackname = self.track.name
		else:
			trackname = None
		return "Race at %s on %s with %s " % (trackname, self.date_time, self.organization)

	class Meta:
		unique_together = ('name', 'date_time', 'track', 'organization', 'user')

	def best_lap_time(self):
		best = None
		for lap in self.laps.values():
			if best is None:
				best = lap['time']
			elif lap['time'] < best:
				best = lap['time']
		return best

	def best_lap_time_for(self, name):
		if self.is_team is None or not(self.is_team):
			return self.best_lap_time()

		laps_by_rider = self.laps_by_rider()
		if not(name in laps_by_rider):
			return None
		laps = laps_by_rider[name]
		best_lap = None
		for lap in laps:
			if best_lap is None:
				best_lap = lap['time']
			elif lap < best_lap:
				best_lap = lap['time']
		return best_lap

	def worst_lap_time(self):
		worst = None
		for lap in self.laps.values():
			if worst is None:
				worst = lap['time']
			elif lap['time'] > worst:
				worst = lap['time']
		return worst

	def average_lap_time(self):
		lapsum = Decimal(0)
		for lap in self.laps.values():
			lapsum = lapsum + lap['time']
		numlaps = len(self.laps.values())
		return lapsum / (Decimal(numlaps))

	def average_lap_time_for(self, name):
		if self.is_team is None or not(self.is_team):
			return self.average_lap_time()

		laps_by_rider = self.laps_by_rider()
		if not(name in laps_by_rider):
			return None
		laps = laps_by_rider[name]

		lapsum = Decimal(0)
		for lap in laps:
			lapsum = lapsum + lap['time']
		numlaps = len(laps)
		return lapsum / (Decimal(numlaps))

	def get_laps(self):
		return self.laps.values().order_by('num')

	def riders(self):
		print "in riders()"
		riders = []
		for change in self.rider_changes.values():
			if 'user_id' in change and change['user_id']:
				print "user_id was in change"
				rider_name = get_user_model().objects.get(pk=change['user_id']).username
				print "rider name is %s" % rider_name
			elif 'rider_name' in change and change['rider_name']:
				rider_name = change['rider_name']
			print "rider_name is %s" % rider_name 
			if not(rider_name in riders):
				riders.append(rider_name)
		return riders

	def rider_changes_by_lap(self):
		changes = {}
		for change in self.rider_changes.values():
			changelapnum = change['num']
			changes[changelapnum] = {}
			if 'rider_name' in change:
				print "found rider_name in change:"
				print change
				changes[changelapnum]['rider_name'] = change['rider_name']
			if 'user_id' in change and change['user_id']:
				changes[change['num']]['user'] = get_user_model().objects.get(pk=change['user_id'])
		return changes

	def laps_by_rider(self):
		result = {}
		last_lap_processed = 10*1000
		for change in RiderChange.objects.filter(race=self).order_by('-num'):
			rider_name = change.get_rider_name()
			if not(rider_name in result):
				result[rider_name] = []
			laps_vqs = Lap.objects.filter(race=self, num__gte=change.num, num__lt=last_lap_processed).order_by('num').values()
			laps = [entry for entry in laps_vqs]
			result[rider_name] = laps + result[rider_name]
			last_lap_processed = change.num
		return result

def get_or_create_race(name=None, date=None, track=None, organization=None, machine_config=None, conditions=None):
	q = Race.objects.filter(name=name, date_time=date, track=track, organization=organization)
	if len(q) > 0:
		return q[0]
	return Race.objects.create(name=name, date_time=date, track=track, organization=organization, machine_config=machine_config, conditions=conditions)

class RiderChange(models.Model):
	race = models.ForeignKey(Race, related_name='rider_changes')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	rider_name = models.CharField(max_length=100, null=True)
	num = models.IntegerField(default=1)

	def get_rider_name(self):
		if self.user:
			return self.user.username
		else:
			return self.rider_name

class Lap(models.Model):
	race = models.ForeignKey(Race, related_name='laps')
	num = models.IntegerField()
	time = models.DecimalField(max_digits=6, decimal_places=3)
