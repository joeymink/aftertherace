from django.test import TestCase
from laps.models import Machine, MachineConfiguration, ConfigurationAttribute

class MachineTest(TestCase):

	def test_save(self):
		m = Machine(name='Ninjette Test', make='Kawi', model='EX250', year=2009)
		m.save()

		mFromDb = Machine.objects.get(id=m.id)
		self.assertTrue(mFromDb.name == 'Ninjette Test')

class MachineConfigurationTest(TestCase):

	def test_save(self):
		m = Machine(name='Ninjette Test', make='Kawi', model='EX250', year=2009)
		m.save()
		c = MachineConfiguration(name='My Config', machine=m)
		c.save()

		mc = MachineConfiguration.objects.get(id=c.id)
		self.assertTrue(c.machine.make == 'Kawi')

		# Test reverse relationship
		readMachine = Machine.objects.get(id=m.id)
		self.assertTrue(readMachine.configurations.all()[0].name == 'My Config')

class ConfigurationAttributeTest(TestCase):

	def test_save(self):
		m = Machine(name='Ninjette Test', make='Kawi', model='EX250', year=2009)
		m.save()
		c = MachineConfiguration(name='My Config', machine=m)
		c.save()
		attr = ConfigurationAttribute(key='chain', value='non-oring 520', machine_config=c)
		attr.save()

		readConfigAttr = ConfigurationAttribute.objects.get(id=attr.id)
		self.assertTrue(readConfigAttr.machine_config.machine.model == 'EX250')

		readMachine = Machine.objects.get(id=m.id)
		self.assertTrue(readMachine.configurations.all()[0].attributes.all()	[0].value == 'non-oring 520')


