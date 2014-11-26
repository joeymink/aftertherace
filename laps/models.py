from django.db import models

# Machine

class Machine(models.Model):
	name = models.CharField(max_length=100, unique=True)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()
	def __unicode__(self):
		return self.name

class MachineConfiguration(models.Model):
	name = models.CharField(max_length=100)
	machine = models.ForeignKey(Machine, related_name='configurations')
	def __unicode__(self):
		return "%s (%s)" % (self.name, self. machine.name)

class ConfigurationAttribute(models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	machine_configurations = models.ManyToManyField(MachineConfiguration)
	def __unicode__(self):
		return "%s: %s" % (self.key, self.value)
	
	class Meta:
		unique_together = ('key', 'value')

# Track

class Track(models.Model):
	name=models.CharField(max_length=100)
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
	machine_config = models.ForeignKey(MachineConfiguration, blank=True, null=True)
	date = models.DateField()
	track = models.ForeignKey(Track)
	organization = models.CharField(max_length=100)
	conditions = models.CharField(max_length=100)
	def __unicode__(self):
		return self.track.name

	class Meta:
		unique_together = ('name', 'date', 'track', 'organization')

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
