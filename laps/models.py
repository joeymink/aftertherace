from django.db import models

# Machine

class Machine(models.Model):
	name = models.CharField(max_length=100)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()
	def __unicode__(self):
		return self.name

class MachineConfiguration(models.Model):
	name = models.CharField(max_length=100)
	machine = models.ForeignKey(Machine, related_name='configurations')

class ConfigurationAttribute(models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	machine_config = models.ForeignKey(MachineConfiguration, related_name='attributes')

# Track

class Track(models.Model):
	name=models.CharField(max_length=100)

# Racer

class Racer(models.Model):
	first = models.CharField(max_length=100)
	last = models.CharField(max_length=100)
	middle = models.CharField(max_length=100)
	dob = models.DateTimeField(null=True)

# Race

class Race(models.Model):
	name = models.CharField(max_length=100)
	machine_config = models.ForeignKey(MachineConfiguration)
	date = models.DateTimeField()
	track = models.ForeignKey(Track)

class Lap(models.Model):
	race = models.ForeignKey(Race, related_name='laps')
	num = models.IntegerField()
	time = models.CharField(max_length=100)	# TODO: need to learn how best to capture this
	racer = models.ForeignKey(Racer, related_name='laps')
