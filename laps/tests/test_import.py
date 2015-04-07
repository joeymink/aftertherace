from django.test import TestCase
from laps import lapimport
from django.contrib.auth import get_user_model

sample_motolaptime_content = '''
<html>
<head>
<title>Laptimes-816A</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body bgcolor="#FFFFFF" text="#000000">
<p>
Class: NJMP 072014<BR>
Date: 07/19/14<BR>
Time: 12:35PM<BR>
SAT RACE 2 GTL EX AM<BR><BR><b>LAPTIMES - No: 816A - JOSEPH MINK</b><BR>
<table width="50%" border="1">
<tr>
<td><b>Index</b></td>
<td><b>Lap</b></td>
<td><b>Laptime</b></td>
</tr>
<tr>
<td><b>1</b></td>
<td>1</td>
<td>02:00.614</td>
<tr>
<tr>
<td><b>2</b></td>
<td>2</td>
<td>01:57.666</td>
<tr>
<tr>
<td><b>3</b></td>
<td>3</td>
<td>01:57.305</td>
<tr>
<tr>
<td><b>4</b></td>
<td>4</td>
<td>01:54.823</td>
<tr>
<tr>
<td><b>5</b></td>
<td>5</td>
<td>01:54.632</td>
<tr>
<tr>
<td><b>6</b></td>
<td>6</td>
<td>01:55.150</td>
<tr>
<tr>
<td><b>7</b></td>
<td>7</td>
<td>01:54.614</td>
<tr>
<tr>
<td><b>8</b></td>
<td>8</td>
<td>01:53.537</td>
<tr>
<tr>
<td><b>9</b></td>
<td>9</td>
<td>01:55.036</td>
<tr>
<tr>
<td><b>10</b></td>
<td>10</td>
<td>01:55.454</td>
<tr>
<tr>
<td><b>11</b></td>
<td>11</td>
<td>01:54.703</td>
<tr>
'''

class MotoLapTimesImport(TestCase):
	def test_creates_model_objects_from_motolaptimes_page(self):
		u,created = get_user_model().objects.get_or_create(username='user1', email='user1@atr.tools')

		url = 'http://motolaptimes.com/2015/RRR030815/SAT%20PRACTICE%20GROUP%201%20ROUND%201-51A-37838.htm'
		parsed_content = lapimport.extract_from_motolaptimes(url)
		r = lapimport.motolaptimes_as_model(parsed_content, u)
		self.assertTrue(len(r.get_laps()) == 8)
		self.assertTrue(r.name == 'SAT PRACTICE GROUP 1 ROUND 1')