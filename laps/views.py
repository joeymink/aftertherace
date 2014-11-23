from laps.models import Race
from django.shortcuts import get_object_or_404, render

def races(request):
	races = Race.objects.all()
	return render(request, 'laps/races.html', {'races': races })

def race(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	return render(request, 'laps/race.html', {'race': race })