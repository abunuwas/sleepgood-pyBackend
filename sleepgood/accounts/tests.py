from django.test import TestCase, Client
from django.contrib.auth.models import User


class registrationUserTest(TestCase):

	def setUp(self):
		self.c = Client()

	def test_registration(self):
		data = {'username': 'carlos',
				'email': 'carlos@carlos.com',
				'password': 'asdf'
				}
		response = self.c.post('/accounts/register', data=data)

		user = User.objects.all()
		print(user)

		print(response.content)

	def test_wrong(self):
		response = self.c.get('/accounts/login')
		print(response)
		print(response.content)

	def test_wrong2(self):
		response2 = self.c.get('/accounts/logout')
		print(response2.content)
