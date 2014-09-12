from django.db import models

class Machine(models.Model):
	name = models.CharField(max_length=100)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()

class MachineConfiguration(models.Model):
	name = models.CharField(max_length=100)
	machine = models.ForeignKey(Machine)

class ConfigurationItem(models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	machine_config = models.ForeignKey(MachineConfiguration)

class Race(models.Model):
	name = models.CharField(max_length=100)
	machine_config = models.ForeignKey(MachineConfiguration)
	date = models.DateTimeField()

class Lap(models.Model):
	race = models.ForeignKey(Race)
	num = models.IntegerField()
	time = models.DateTimeField('date published')
