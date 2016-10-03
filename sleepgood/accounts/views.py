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

		user = authenticate(username=request.data['username'], password=request.data['password'])

		if user is not None:
			if user.is_active:
				login(request, user)
				wrapper = jwtWrapper();
				encoded = wrapper.create(user.id)
				data = {
					'token_key': str(encoded.decode("utf-8")),
					'username': str(user.get_username()),
					'userId': str(user.id)
				}
				return JsonResponse(data)
			else:
				HttpResponse('You are not active')
		else:
			return HttpResponse(status.HTTP_401_UNAUTHORIZED)


def delete(self, request, format=None):  # Delete user token (sign out)
	print("delete")
	return 0;


class Users(APIView):
	http_method_names = ['post', 'get']
	permission_classes = (permissions.AllowAny,)
	parser_classes = (JSONParser,)


	def get(self, request):  # get user info - profile
		get_token(request)
		data = {}
		for key, value in dict(request.META).items():
			data[str(key)] = str(value)
		return JsonResponse(data)

	def post(self, request):

		if len(dict(request.data).items()) == 0:
			return HttpResponse(status.HTTP_401_UNAUTHORIZED)

		username = request.data['username']
		password = request.data['password']
		email = request.data['email']

		# check if e-mail already exists
		if User.objects.filter(email=email).exists():
			return HttpResponse('user already exists', status.HTTP_409_CONFLICT)

		# check if e-mail already exists (FIX: username should be allowed)
		# http://django-authtools.readthedocs.io/en/latest/how-to/migrate-to-a-custom-user-model.html
		if User.objects.filter(username=username).exists():
			return HttpResponse('username already exists', status.HTTP_409_CONFLICT)

		# sign out new user
		new_user = User(username=username, email=email)
		new_user.set_password(password)
		try:
			new_user.save()
		except RuntimeError:
			return Response('error on token parsing.', status=status.HTTP_400_BAD_REQUEST)

		# login user automatically and return new JWT key
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				wrapper = jwtWrapper();
				encoded = wrapper.create(user.id)
				data = {
					'token_key': str(encoded.decode("utf-8")),
					'username': str(user.get_username()),
					'userId': str(user.id)
				}
				return JsonResponse(data)
			else:
				HttpResponse('You are not active')
		else:
			return HttpResponse(status.HTTP_401_UNAUTHORIZED)


	# def post(self, request):  # create a new user - sign up
	# 	username, email, password = request.POST['username'], request.POST['email'], request.POST['password']
	# 	new_user = User(username=username, email=email)
	# 	new_user.set_password(password)
	# 	new_user.save()
	# 	user = authenticate(username=username, password=password)
	# 	if user is not None:
	# 		if user.is_active:
	# 			login(request, user)
	# 			data = {}
	# 			for key, value in dict(request.META).items():
	# 				data[str(key)] = str(value)
	# 			return JsonResponse(data)
	# 		# return HttpResponse('Good!')
	# 		else:
	# 			HttpResponse('You are not active')
	# 	else:
	# 		HttpResponse('The account does not exist')

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
