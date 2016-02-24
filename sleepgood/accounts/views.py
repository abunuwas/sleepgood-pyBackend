from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


class Register(View):
	http_method_names = ['post']

	def post(self, request):
		username, email, password = request.POST['username'], request.POST['email'], request.POST['password']
		new_user = User(username=username, email=email)
		new_user.set_password(password)
		new_user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse('Good!')
			else: 
				HttpResponse('You are not active')
		else:
			HttpResponse('The account does not exist')
		


@login_required(login_url='/')
def login(request):
	return HttpResponse('You are loggedd in')

def logout(request):
	return HttpResponse('You are in logout') 
