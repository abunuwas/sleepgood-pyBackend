from django.shortcuts import render
from django.http import HttpResponse

import uuid


def generateUUID(username, date):
    uuidValue = uuid.uuid3(uuid.NAMESPACE_DNS, username + date)
    return str(uuidValue)

def indexView(request):
	return HttpResponse('You are in index view!')

