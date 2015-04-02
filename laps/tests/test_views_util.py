from django.test import TestCase
from laps import util as util
from decimal import Decimal

class HomePageTest(TestCase):

	def test_simple_interpret_time(self):
		num_seconds = util.interpret_time('1:30:500')
		self.assertTrue((num_seconds - Decimal(90.5)) < 0.0001)