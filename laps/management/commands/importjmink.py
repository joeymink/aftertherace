from django.core.management.base import BaseCommand
import csv, os
from laps.models import Race, Racer, Track

class Command(BaseCommand):
	help = "import's a csv version of Joey's lap times Google doc"

	def handle(self, *args, **options):
		csv_file = args[0]
		if not(os.path.exists(csv_file)):
			raise CommandError("%s does not exist" % csv_file)
		with open(csv_file, 'rb') as f:
			csvreader = csv.reader(f)
			index = {'Track':0, 'Date':1, 'Time':2, 'Bike':3, 'Front sprocket':4, 'Rear sprocket':5, 'Chain':6, 'Jet kit':7, 'Tires':8, 'Organization':9, 'Lap number':10, 'Lap total':11, 'Event':12, 'Weather':13, 'Source':14}
			racer, created = Racer.objects.get_or_create(first="Joey", last="Mink")
			isfirstrow = True
			for row in csvreader:
				if not(isfirstrow):
					track, created = Track.objects.get_or_create(name=row[index['Track']])

					raw_date = row[index['Date']]
					month_day_year = raw_date.split('/')
					yyyy_mm_dd = "%s-%s-%s" % (month_day_year[2], month_day_year[0], month_day_year[1])
					race, created = Race.objects.get_or_create(name=row[index['Event']], date=yyyy_mm_dd, track=track)
				else:
					isfirstrow = False