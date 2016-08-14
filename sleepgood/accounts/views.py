import jwt
import base64
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.generic import View
from rest_framework.parsers import JSONParser
from requests import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from rest_framework import viewsets, status, mixins, generics, permissions
from .jwtWrapper import jwtWrapper

class Sessions(APIView):
	permission_classes = (permissions.AllowAny,)
	parser_classes = (JSONParser,)

	def post(self, request, format=None):  # Create user new token (login in)

		if len(dict(request.data).items()) == 0:
			return HttpResponse(status.HTTP_401_UNAUTHORIZED)
		data = {}
		for key, value in dict(request.data).items():
			data[str(key)] = str(value)
		user = authenticate(username=data['username'], password=data['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				encoded = jwtWrapper.createToken()
				data = {'token_key': str(encoded.decode("utf-8"))}
				return JsonResponse(data)
			else:
				HttpResponse('You are not active')
		else:
			return HttpResponse(status.HTTP_401_UNAUTHORIZED)


def delete(self, request, format=None):  # Delete user token (sign out)
	print("delete")
	return 0;


class User(View):
	http_method_names = ['post', 'get']

	def get(self, request):  # get user info - profile
		get_token(request)
		data = {}
		for key, value in dict(request.META).items():
			data[str(key)] = str(value)
		return JsonResponse(data)

	def post(self, request):  # create a new user - sign up
		username, email, password = request.POST['username'], request.POST['email'], request.POST['password']
		new_user = User(username=username, email=email)
		new_user.set_password(password)
		new_user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				data = {}
				for key, value in dict(request.META).items():
					data[str(key)] = str(value)
				return JsonResponse(data)
			# return HttpResponse('Good!')
			else:
				HttpResponse('You are not active')
		else:
			HttpResponse('The account does not exist')

	def delete(self):
		return 0  # delete an existing user - profile

	def put(self):
		return 0  # modify an existng user - profile

#
# def expose(request):
# 	get_token(request)
# 	#hFwr0EKBGomGwOesoWhQ9FpiMAvKNA5g
# 	#csrftoken=hFwr0EKBGomGwOesoWhQ9FpiMAvKNA5g
# 	#output = ''
# 	#for key, value in dict(request.META).items():
# 	#	output += str(key) + ' ========> ' + str(value) + '<br/>'
# 	data = {}
# 	for key, value in dict(request.META).items():
# 		data[str(key)] = str(value)
# 	return JsonResponse(data)
