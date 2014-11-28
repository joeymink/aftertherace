from laps.models import Machine, Race
from django.shortcuts import get_object_or_404, render

def races(request):
	races = Race.objects.all().order_by('date')
	years = []
	dates = []
	race_by_date={}
	for race in races:
		year = race.date.year
		if not(year in years):
			years.append(year)
		if not(race.date in dates):
			dates.append(race.date)
	return render(request, 'laps/races.html', {
		'races':races,
		'years':years,
		'dates':dates })

def race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	return render(request, 'laps/race.html', {'race': race })

def machine(request, machine_id):
	machine = get_object_or_404(Machine, pk=machine_id)
	return render(request, 'laps/machine.html', {'machine': machine })