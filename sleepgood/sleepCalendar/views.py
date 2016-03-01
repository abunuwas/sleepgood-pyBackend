from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.views.generic import View
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets

import uuid
import json
import datetime
import dateutil.parser

from .models import Day
from .serializers import UserSerializer, GroupSerializer


def indexView(request):
	return HttpResponse('You are in index view!')

@require_http_methods(["GET"])
def getCalendarEntriesByYear(request, year):
	'''
	Returns all calendar entries for a given year. Only accepts get methods.
	If a different method is used in the request, returns a 405 status code. 
	'''
	queryset = Calendar.objects.all()
	data = {}
	for query in queryset:
		date = query.date
		date = '{}-{:02d}-{}'.format(date.year, date.month, date.day)
		data[date] = {'id': query.pk,
		                    'sleepingQuality': query.sleepingQuality,
		                    'tirednessFeeling': query.tirednessFeeling,
		                    'userId': query.user.id,
		                    'date': str(query.date),
		                    'uuid': query.uuid}
	data = json.dumps(data)
	return HttpResponse(data, content_type='application/json')


def getDatetimeFromISO(dateISO):
	'''
	Expects a date string in ISO format as returned, for example, by the JavaScript function 
	toISOString(), and returns a datetime object, using the third party library python-dateutil.
	If the data doesn't follow a valid date format, it returns an HTTP 400 response. 
	Examples: 
	getDatetimeFromISO("2016-02-09T22:41:21.955Z) => datetime.datetime(2016, 2, 9, 22, 41, 21, 955000, tzinfo=tzutc()).
	getDatetimeFromISO("2016-02-09") => datetime.datetime(2016, 2, 9, 0, 0). 
	getDatetimeFromISO("asdf") => HTTP 404 error code. 
	'''
	try:
		return dateutil.parser.parse(dateISO)
	except ValueError:
		raise SuspiciousOperation("Date format is not valid!")

def generateUUID(userId, date):
	'''
	Returns an md5 hash using string which combines the user id plus the calendar date of the event
	as a way to generate a unique value. Not sure yet, though, if this is the best approach...
	'''
	currentMilliseconds = datetime.datetime.now().timestamp()
	uuidValue = uuid.uuid3(uuid.NAMESPACE_DNS, userId + date + str(currentMilliseconds))
	return str(uuidValue)


class InsertUpdateDelete(View):
	http_method_names = ['post', 'put', 'delete']

	def post(self, request):
		items = dict(request.POST.items())
		date = getDatetimeFromISO(items['date'])
		entryUUID = generateUUID(str(items['_userId']), str(date))
		user = User.objects.get(pk=items['_userId'])
		newEntry = Calendar(user=user,
			                date=date,
			                sleepingQuality=items['sleepingQuality'],
			                tirednessFeeling=items['tirednessFeeling'],
			                uuid=entryUUID,
			                date_created=timezone.now(),
			                date_modified=timezone.now()
			                )
		newEntry.save()
		
		responseData = Calendar.objects.get(uuid=entryUUID)
		responseData = responseData.getDict()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						'responseData': responseData						
						}
		return JsonResponse(returnJson)

	def put(self, request):
		'''
		The request object cannot have a PUT attribute, so the data that comes in a  put request
		cannot be accessed by calling request.PUT. Instead, we need to access the body of the
		request and decode it from bytes into strings, and read its data with the json.loads function.
		We then convert this data into a Python dictionary. 
		'''
		inputData = dict(json.loads(request.body.decode()))
		entryUUID = inputData['UUID']
		dbEntry = Calendar.objects.get(uuid=entryUUID)
		dbEntry.sleepingQuality = inputData['sleepingQuality']
		dbEntry.tirednessFeeling = inputData['tirednessFeeling']
		dbEntry.date_modified = timezone.now()
		dbEntry.save()
		responseData = Calendar.objects.get(uuid=entryUUID)
		responseData = responseData.getDict()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						'responseData': responseData
						}
		return JsonResponse(returnJson)

	def delete(self, request):
		'''
		The request object cannot have a DELETE attribute, so the data that comes in a  put request
		cannot be accessed by calling request.DELETE. Instead, we need to access the body of the
		request and decode it from bytes into strings, and read its data with the json.loads function.
		We then convert this data into a Python dictionary. 
		'''
		requestData = dict(json.loads(request.body.decode()))
		entryUUID = requestData['UUID']
		dbEntry = Calendar.objects.get(uuid=entryUUID)
		dbEntry.delete()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						}
		return JsonResponse(returnJson)

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	'''
	API endpoint that allows groups to be viewed or edied.
	'''
	queryset = Group.objects.all()
	serializer_class = GroupSerializer






