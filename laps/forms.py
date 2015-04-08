from django import forms
from templatetags.lap_extras import format_lap_time
from laps.models import Lap, Machine, Race, Racer, Track

class EditRaceForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)
	organization = forms.CharField(label='Organization', max_length=100, required=False)
	date_time = forms.DateTimeField(label="Date")
	machine_name = forms.ChoiceField(label='Machine')
	track_name = forms.ChoiceField(label='Track')
	num_laps = forms.IntegerField(label='# Laps', min_value=1)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(EditRaceForm, self).__init__(*args, **kwargs)
		self.set_choices(user)

	def set_choices(self, user):
		choices = []
		for n in Machine.objects.filter(user=user).values('name').order_by('name'):
			choices.append( (n['name'], n['name']) )
		self.fields['machine_name'].choices = choices
		
		choices = []
		for t in Track.objects.all().values('name').order_by('name'):
			choices.append( (t['name'], t['name']) )
		self.fields['track_name'].choices = choices

class EditLapsForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.num_laps = int(kwargs.pop('num_laps'))
		laps = kwargs.pop('laps')
		super(EditLapsForm, self).__init__(*args, **kwargs)
		for i in xrange(1, self.num_laps + 1):
			lap = None
			if not(laps is None):
				for l in laps:
					if l.num == i:
						lap = l
						break
			self.fields["lap%d" % i] = forms.RegexField(
				label="Lap %d" % i,
				regex='[0-9]+:[0-9]{2}:[0-9]{3}',
				required=False)
			if not(lap is None):
				self.fields["lap%d" % i].initial = format_lap_time(lap.time)

	def get_lap_dict(self):
		laps_dict = {}
		for key, value in self.cleaned_data.iteritems():
			if key.startswith('lap'):
				if value.strip():
					lap_num = int(key[3:]) # all characters after 'lap'
					laps_dict[lap_num] = value
					print "found lap number %d with value %s" % (lap_num, value)
		return laps_dict

	def num_laps(self):
		return self.num_laps

class AddConfigurationAttributeToRaceForm(forms.Form):
	key = forms.CharField(label='Key', max_length=100)
	value = forms.CharField(label='Value', max_length=100)

class EditMachineForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)
	make = forms.CharField(label='Make', max_length=100)
	model = forms.CharField(label='Model', max_length=100)
	year = forms.IntegerField(label='Year', min_value=1)

class ImportMotolaptimesForm(forms.Form):
	url = forms.URLField(label='Race Results URL', required=True)
