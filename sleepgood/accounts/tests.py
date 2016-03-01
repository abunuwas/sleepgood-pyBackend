from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.http import HttpResponse, HttpRequest 

from .views import Register, login, logout

class registrationUserTest(TestCase):

	def setUp(self):
		self.c = Client()
		self.factory = RequestFactory()
		self.jacob = User.objects.create_user(
			username='jacob', email='j@j.com', password='secret')

	def test_registration(self):
		data = {'username': 'carlos',
				'email': 'carlos@carlos.com',
				'password': 'asdf'
				}

		response = self.c.post('/accounts/register', data=data)

		carlos = User.objects.all()
		print(carlos)
		print(response.content)

	def test_sessions(self):
		self.c.login(username='jacob', email='j@j.com')
		response = self.c.get('/accounts/login')
		print('Result after login ', response)
		jacob = User.objects.get(email='j@j.com')
		session = self.c.session
		session['member_id'] = jacob.pk
		print(dict(session))
		#response = logout(request)
		#print(response)
		#print('Request data is', request.META)

	def test_wrong(self):
		response = self.c.get('/accounts/login')
		print(response)
		print(response.content)

	def test_wrong2(self):
		response2 = self.c.get('/accounts/logout')
		print(response2.content)
