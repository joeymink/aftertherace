from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from laps.models import Machine
from laps.views import RacesByYear
from laps.views.user_util import assert_user_logged_in
import laps.forms

def machine(request, username, machine_id):
	user = get_object_or_404(get_user_model(), username=username)
	machine = get_object_or_404(Machine, pk=machine_id, user=user)
	races = RacesByYear()
	races.get_races(Q(machine_config__machine=machine))
	return render(request, 'laps/machine.html', {
		'racer' : user.username,
		'machine': machine,
		'races':races.races,
		'years':races.years,
		'dates':races.dates})

def machines(request, username):
	user = get_object_or_404(get_user_model(), username=username)
	machines = Machine.objects.filter(user=user)
	return render(request, 'laps/machines.html', {
		'racer' : user.username,
		'machines': machines})

@login_required
def create_machine(request, username):
	user = assert_user_logged_in(username, request)

	if request.method == 'POST':
		form = laps.forms.EditMachineForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				machine = Machine()
				machine.name = form.cleaned_data['name']
				machine.make = form.cleaned_data['make']
				machine.model = form.cleaned_data['model']
				machine.year = form.cleaned_data['year']
				machine.user = user
				machine.save()
				return HttpResponseRedirect(reverse('laps:machines', args=(username,)))
	else:
		form = laps.forms.EditMachineForm()
	return render(request, 'laps/new_machine.html', { 'form':form, 'racer': user.username })

@login_required
def edit_machine(request, username, machine_id):
	user = assert_user_logged_in(username, request)
	machine = get_object_or_404(Machine, pk=machine_id)
	if not(machine.user == user):
		raise PermissionDenied

	if request.method == 'POST':
		form = laps.forms.EditMachineForm(request.POST)
		if form.has_changed():
			if form.is_valid():
				machine.name = form.cleaned_data['name']
				machine.make = form.cleaned_data['make']
				machine.model = form.cleaned_data['model']
				machine.year = form.cleaned_data['year']
				machine.save()
				return HttpResponseRedirect(reverse('laps:machine', args=(username, machine.id)))
	else:
		initial_form_values = machine.__dict__
		form = laps.forms.EditMachineForm(initial_form_values)
	return render(request, 'laps/edit_machine.html', { 'form':form, 'machine':machine, 'racer': username })
