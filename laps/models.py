from django.db import models

# Machine

class Machine(models.Model):
	name = models.CharField(max_length=100, unique=True)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()
	def __unicode__(self):
		return self.name

	def num_laps(self):
		return Lap.objects.filter(race__machine_config__machine=self).count()

	def races(self):
		return Race.objects.filter(machine_config__machine=self).order_by('date')

	def first_race(self):
		return Lap.objects.filter(race__machine_config__machine=self).order_by('race__date')[0].race

	def last_race(self):
		return Lap.objects.filter(race__machine_config__machine=self).order_by('-race__date')[0].race

	def unique_configuration_keys(self):
		keys = []
		for c in self.configurations.all():
			for key in ConfigurationAttribute.objects.filter(machine_configurations__in=[c.id]).order_by('key').values('key').distinct():
				if not(key in keys):
					keys.append(key)
		return keys

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
		print config_list
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

# Racer

class Racer(models.Model):
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
	date = models.DateField()
	track = models.ForeignKey(Track, related_name="races")
	organization = models.CharField(max_length=100)
	conditions = models.CharField(max_length=100)
	def __unicode__(self):
		return self.track.name

	class Meta:
		unique_together = ('name', 'date', 'track', 'organization')

	def best_lap_time(self):
		best = None
		for lap in self.laps.values():
			if best is None:
				best = lap['time']
			elif lap['time'] < best:
				best = lap['time']
		return best


def get_or_create_race(name=None, date=None, track=None, organization=None, machine_config=None, conditions=None):
	q = Race.objects.filter(name=name, date=date, track=track, organization=organization)
	if len(q) > 0:
		return q[0]
	return Race.objects.create(name=name, date=date, track=track, organization=organization, machine_config=machine_config, conditions=conditions)

class Lap(models.Model):
	race = models.ForeignKey(Race, related_name='laps')
	num = models.IntegerField()
	time = models.DecimalField(max_digits=6, decimal_places=3)
	racer = models.ForeignKey(Racer, related_name='laps')
