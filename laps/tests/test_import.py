from django.test import TestCase
from laps import lapimport
from django.contrib.auth import get_user_model

class MotoLapTimesImport(TestCase):
	def test_creates_model_objects_from_motolaptimes_page(self):
		u,created = get_user_model().objects.get_or_create(username='user1', email='user1@atr.tools')

		url = 'http://motolaptimes.com/2015/RRR030815/SAT%20PRACTICE%20GROUP%201%20ROUND%201-51A-37838.htm'
		parsed_content = lapimport.extract_from_motolaptimes(url)
		r = lapimport.motolaptimes_as_model(parsed_content, u)
		self.assertTrue(len(r.get_laps()) == r.num_laps)
		self.assertTrue(len(r.get_laps()) == 8)
		self.assertTrue(r.name == 'SAT PRACTICE GROUP 1 ROUND 1')