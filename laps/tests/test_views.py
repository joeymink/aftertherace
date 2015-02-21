from django.core.urlresolvers import resolve
from django.test import TestCase
from laps import views as laps_views
from django.contrib.auth import views as auth_views
from django.http import HttpRequest
from django.core.urlresolvers import reverse

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, laps_views.index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = laps_views.index(request)
        #self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        #self.assertTrue(response.content.endswith(b'</html>'))
        self.assertIn(reverse('login'), response.content) # ensure there's a login link


class LoginPageTest(TestCase):

    def test_login_url_resolves_to_login_view(self):
        found = resolve('/accounts/login/')
        self.assertEqual(found.func, auth_views.login)

    # Need to find a way to submit property csrf token
    #def test_login_page_returns_correct_html(self):
    #    request = HttpRequest()
    #    response = auth_views.login(request)
    #    self.assertIn(reverse('password_reset'), response.content) # ensure pwd reset link


class PasswordResetPageTest(TestCase):

    def test_password_reset_url_resolves_to_password_reset_view(self):
        found = resolve('/accounts/password_reset/')
        self.assertEqual(found.func, auth_views.password_reset)

    # Complains about csrf token - but this is not a form submission - hmmm...
    #def test_password_reset_page_returns_correct_html(self):
    #    request = HttpRequest()
    #    response = auth_views.password_reset(request)
    #    self.assertIn('Reset my password', response.content)


class PasswordResetDonePageTest(TestCase):

    def test_password_reset_done_url_resolves_to_login_view(self):
        found = resolve('/accounts/password_reset/mailed/')
        self.assertEqual(found.func, auth_views.password_reset_done)

    # Need to find a way to submit property csrf token
    #def test_password_reset_done_page_returns_correct_html(self):
    #    request = HttpRequest()
    #    response = auth_views.password_reset_done(request)
    #    self.assertIn('A password reset e-mail has been sent', response.content)
    #    self.assertIn(reverse('index'), response.content) # ensure home link


class PasswordResetConfirmPageTest(TestCase):

	def test_password_reset_confirm_url_resolves(self):
		found = resolve('/accounts/password_reset/MTQ-3zg-65708870f652336689ce/')
		self.assertEqual(found.func, auth_views.password_reset_confirm)


class PasswordResetCompletePageTest(TestCase):

	def test_password_reset_confirm_url_resolves(self):
		found = resolve('/accounts/password_reset/complete/')
		self.assertEqual(found.func, auth_views.password_reset_complete)

