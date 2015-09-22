from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_lap_time(time_in_seconds):
	if time_in_seconds is None:
		return "None"
	print "type is %s" % type(time_in_seconds)
	print "value is '%s'" % time_in_seconds
	minutes = int(time_in_seconds/60)
	seconds = (time_in_seconds - minutes*60)
	thousandths = (time_in_seconds * 1000) % 1000
	return "%d:%02d:%03d" % (minutes, seconds, thousandths)

@register.filter
def best_lap(laps_list):
	best = None
	for lap in laps_list:
		if best is None:
			best = lap['time']
		elif lap['time'] < best:
			best = lap['time']
	return format_lap_time(best)

@register.filter
def worst_lap(laps_list):
	worst = None
	for lap in laps_list:
		if worst is None:
			worst = lap['time']
		elif lap['time'] > worst:
			worst = lap['time']
	return format_lap_time(worst)

@register.filter
def average_lap(laps_list):
	lapsum = Decimal(0)
	for lap in laps_list:
		lapsum = lapsum + lap['time']
	numlaps = len(laps_list)
	return format_lap_time(lapsum / (Decimal(numlaps)))

@register.filter
def idify(str):
	return str.replace(' ', '_')
