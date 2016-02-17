from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.views.generic import View
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User

import uuid
import json
import datetime
import dateutil.parser

from .models import Calendar


def indexView(request):
	return HttpResponse('You are in index view!')

def getCalendarEntriesByYear(request, userId, year):
	queryset = Calendar.objects.all()
	data = {}
	for query in queryset:
		date = query.date
		date = '{}-{:02d}-{}'.format(date.year, date.month, date.day)
		data[date] = {'id': query.pk,
		                    'sleepingQuality': query.sleepingQuality,
		                    'tirednessFeeling': query.tirednessFeeling,
		                    'userId': query.userId,
		                    'date': str(query.date),
		                    'uuid': query.uuid}
	data = json.dumps(data)
	#data = serializers.serialize('json', query)
	return HttpResponse(data, content_type='application/json')
	#return HttpResponse('You are in index view!')


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
		## WARNING: this is a naive datetime; it should include also time zone information. 
		date = getDatetimeFromISO(items['date'])
		entryUUID = generateUUID(str(userId), str(date))
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
		
		returnEntry = Calendar.objects.get(uuid=entryUUID)
		returnEntryDict = returnEntry.getDict()
		returnEntryDict['operation'] = 'sucess'
		return JsonResponse(returnEntryDict)

	def put(self, request, userId):
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
		# This should actually return a json reporting sucess or failure
		return redirect('/')

	def delete(self, request, userId):
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
		# This should actually return a json reporting sucess or failure
		return redirect('/')




