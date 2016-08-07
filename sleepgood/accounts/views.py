import jwt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.generic import View
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView


class Sessions(APIView):

	def post(self, request, format=None): #Create user new token (login in)
		print("post")
		# get user credentials from json payload username / password")
		user_exist = 1  # workaround
		if user_exist:
			payload = {'iss': 'sleepdiary.io', 'sub:': 'Vicens'}
			encoded = jwt.encode(payload, 'secret', algorithm='HS256')
			return HttpResponse(encoded)

	def delete(self, request, format=None): #Delete user token (sign out)
		print("delete")
		return 0;


class User(View):
	http_method_names = ['post', 'get']

	def get(self, request): #get user info - profile
		get_token(request)
		data = {}
		for key, value in dict(request.META).items():
			data[str(key)] = str(value)
		return JsonResponse(data)

	def post(self, request): #create a new user - sign up
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
