from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

def assert_user_logged_in(username, request):
	user = get_object_or_404(get_user_model(), username=username)
	if not(user.username == request.user.username):
		raise PermissionDenied
	return user