from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import uuid
import json

from .models import Calendar


def generateUUID(username, date):
    uuidValue = uuid.uuid3(uuid.NAMESPACE_DNS, username + date)
    return str(uuidValue)

def indexView(request):
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

b = '''
{
 "2016-02-02": {
 "ID": "56B0C07ED4C6CD3485EFD066",
 "SLEEPINGQUALITY": "GOOD",
 "TIREDNESSFEELING": "BAD",
 "USERID": 1,
 "DATE": “2016-02-02T00:00:00.000Z"
 “9138C4F6-42DE-4918-89DF-957AF0F6E17D"
 },
'''