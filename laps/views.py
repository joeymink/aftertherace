from laps.models import Race
from django.http import HttpResponse
from django.shortcuts import render

def races(request):
	races = Race.objects.all()
	return render(request, 'laps/races.html', {'races': races })