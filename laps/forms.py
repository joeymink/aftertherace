from django import forms

class EditRaceForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)