from django.test import TestCase
from laps.models import Machine, MachineConfiguration

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


