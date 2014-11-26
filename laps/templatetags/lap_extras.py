from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_lap_time(time_in_seconds):
	minutes = int(time_in_seconds/60)
	seconds = (time_in_seconds - minutes*60)
	thousandths = (time_in_seconds * 1000) % 1000
	return "%d:%02d:%03d" % (minutes, seconds, thousandths)