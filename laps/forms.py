from django import forms
from templatetags.lap_extras import format_lap_time

class EditRaceForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)
	num_laps = forms.IntegerField(label='# Laps')

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
			self.fields["lap%d" % i] = forms.CharField(label="lap%d" % i, required=False)
			if not(lap is None):
				self.fields["lap%d" % i].initial = format_lap_time(lap.time)

	def get_lap_dict(self):
		laps_dict = {}
		for key, value in self.cleaned_data.iteritems():
			if key.startswith('lap'):
				if value.strip():
					lap_num = int(key[3:])
					laps_dict[lap_num] = value
					print "found lap number %d with value %s" % (lap_num, value)
		return laps_dict

	def num_laps(self):
		return self.num_laps
