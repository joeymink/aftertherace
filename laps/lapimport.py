import requests
import re
from bs4 import BeautifulSoup

def extract_from_motolaptimes(url):
	r = requests.get(url)
	return parse_motolaptimes_content(r.text)

def parse_motolaptimes_content(content):
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

