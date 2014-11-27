from laps.models import Race
from django.shortcuts import get_object_or_404, render

def races(request):
	races = Race.objects.all().order_by('date')
	race_by_date={}
	for race in races:
		year = race.date.year
		if not(year in race_by_date):
			race_by_date[year] = {}
		if not(race.date in race_by_date[year]):
			race_by_date[year][race.date] = []
		race_by_date[year][race.date].append(race)
	print race_by_date
	return render(request, 'laps/races.html', {'races_by_date': race_by_date })

def race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	return render(request, 'laps/race.html', {'race': race })