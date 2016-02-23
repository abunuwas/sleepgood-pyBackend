from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User

class Register(View):
	http_method_names = ['post']

	def post(request, email, username):
		new_user = User(email=email, username=username)
		new_user.save()


def login(request):
	pass

def logout(request):
	pass 
