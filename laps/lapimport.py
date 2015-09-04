import requests
import re
from bs4 import BeautifulSoup
from laps.models import Lap, Race
import datetime
from laps import util

def extract_from_motolaptimes(url):
	'''
		GETs the given motolaptimes url
		and extracts its contents
	'''
	r = requests.get(url)
	return parse_motolaptimes_content(r.text)

def parse_motolaptimes_content(content):
	'''
		parses the content from a motolaptimes
		race page
	'''

	parsed_content = {}
	
	#Date: 07/19/14
	m = re.search(r'.*Date: (.*).BR.', content)
	if not(m is None):
		parsed_content['date'] = m.group(1)
	
	#Time: 12:35PM<BR>
	m = re.search(r'.*Time: (.*).BR.', content)
	if not(m is None):
		parsed_content['time'] = m.group(1)
	
	#SAT RACE 2 GTL EX AM<BR><BR><b>LAPTIMES
	m = re.search(r'^(.*).BR..BR..b.LAPTIMES', content, re.MULTILINE)
	if not(m is None):
		parsed_content['name'] = m.group(1)

	laps = []
	soup = BeautifulSoup(content)
	tds = soup.find_all('td')
	for i in range(len(tds)):
		# 1st 3 tds are headers
		if i < 3:
			continue
		# lap times are 3rd value in each row, 1st is index 5
		# 5, 8, 11, ...
		elif ((i - 5) % 3) != 0:
			continue
		laps.append(tds[i].string)
	parsed_content['laps'] = laps
	
	return parsed_content

def motolaptimes_as_model(parsed_content, user):
	'''
		converts parsed motolaptimes content to
		model objects and persists them
	'''
	if not('date' in parsed_content):
		parsed_content['date'] = '9/4/15'
	if not('time' in parsed_content):
		parsed_content['time'] = '12:00PM'
	if not('name' in parsed_content):
		parsed_content['name'] = 'Unnamed Race'

	date_str = "%s %s" % (parsed_content['date'], parsed_content['time'])
	print "date_str=%s" % date_str
	date = datetime.datetime.strptime(date_str, '%m/%d/%y %H:%M%p')
	num_laps = len(parsed_content['laps'])
	r = Race(user=user, name=parsed_content['name'], date_time=date, num_laps=num_laps)
	r.save()

	for i in range(num_laps):
		lapstr = parsed_content['laps'][i]
		lapstr = lapstr.replace('.', ':')
		laptime = util.interpret_time(lapstr)
		lap, created = Lap.objects.get_or_create(race=r, num=i+1, time=laptime)

	return r

def extract_from_text(laptext):
	'''
		parses race data from text (only laps, currently)
	'''
	parsed_content = {}
	parsed_content['laps'] = laptext.split()
	return parsed_content
