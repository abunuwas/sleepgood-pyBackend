from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone

import uuid
import json
import datetime

from .models import Calendar


def indexView(request):
	return HttpResponse('You are in index view!')

def getCalendarEntriesByYear(request, userId, year):
	queryset = Calendar.objects.all()
	data = {}
	for query in queryset:
		date = query.date
		date = '{}-{}-{}'.format(date.year, date.month, date.day)
		data[date] = {'ID': query.pk,
		                    'SLEEPINGQUALITY': query.sleepingQuality,
		                    'TIREDNESSFEELING': query.tirednessFeeling,
		                    'UESRID': query.userId,
		                    'DATE': str(query.date),
		                    'UUID': query.uuid}
	data = json.dumps(data)
	#data = serializers.serialize('json', query)
	return HttpResponse(data, content_type='application/json')
	#return HttpResponse('You are in index view!')


def getYearMonthDayFromISO(dateISO):
	'''
	Expects a date in ISO format as returned by the JavaScript function toISOString().
	For example: 2016-02-09T22:41:21.955Z => 2016-02-09.
	'''
	return dateISO[:10].strip()

def makeDatetimeObject(date):
	'''
	Expects a date string in the following format: 2006-12-01 and returns a datetime object of the 
	following format: datetime.datetime(2016, 12, 1)
	'''
	dateList = date.strip().split('-')
	dateIntegers = [int(i) for i in dateList]
	return datetime.datetime(dateIntegers[0], dateIntegers[1], dateIntegers[2])

def getDate(date):
	'''
	Helper function that combines the getYearMonthDayFromISO() and the makeDatetimeObject()
	to provide the date format expected by the database model. 
	'''
	date = getYearMonthDayFromISO(date)
	date = makeDatetimeObject(date)
	return date

def generateUUID(username, date):
	'''
	Returns an md5 hash using string which combines the username plus the calendar date of the event
	as a way to generate a unique value. Not sure yet, though, if this is the best approach...
	'''
	uuidValue = uuid.uuid3(uuid.NAMESPACE_DNS, username + date)
	return str(uuidValue)

def insertCalendarEntry(request, userId):
	if request.method == 'GET':
		return HttpResponse('You should use a post method!')
	if request.method == 'POST':
		items = dict(request.POST.items())
		## WARNING: this is a naive datetime; it should include also time zone information. 
		date = getDate(items['date'])
		dateString = getYearMonthDayFromISO(items['date'])
		entryUUID = generateUUID(str(userId), dateString)
		newEntry = Calendar(userId=userId,
			                date=date,
			                sleepingQuality=items['sleepingQuality'],
			                tirednessFeeling=items['tirednessFeeling'],
			                uuid=entryUUID
			                )
		newEntry.save()
		return redirect('/')
