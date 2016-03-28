from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.views.generic import View
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import json
import datetime
import dateutil.parser

from .models import Day
from .serializers import UserSerializer, GroupSerializer, DaySerializer
from .permissions import IsOwnerOrReadOnly


def indexView(request):
	return HttpResponse('You are in index view!')

#######################################################################


@api_view(['GET'])
def get_calendar_entries_api(request, year, format=None):
	entries = Day.objects.filter(date__year=year)
	serializer = DaySerializer(entries, many=True)
	return JsonResponse(serializer.data[0])

class GetCalendarEntries(mixins.ListModelMixin,
						generics.GenericAPIView):
	queryset = Day.objects.all()
	lookup_field = 'date__year'
	serializer_class = DaySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly,)

	def list(self, request, *args, **kwargs):
		year = kwargs['date__year']
		user = request.user
		userId = user.id
		queryset = Day.objects.filter(user=userId, date__year=year)
		serializer = self.get_serializer(queryset, many=True)
		return_data = {}
		for result in serializer.data:
			date = result['date'][:10]
			# I think that the user id is actually not necessary at all, since it's included
			# in the authentication. 
			#del result['user']
			return_data[date] = result	    
		return Response(return_data)
	    #return Response(serializer.data[0])

	def get(self, request, *args, **kwargs):
		result_set = self.list(request, *args, **kwargs)
		return result_set

class InsertUpdateDeleteAPI(mixins.RetrieveModelMixin,
							mixins.CreateModelMixin,
							mixins.UpdateModelMixin,
							mixins.DestroyModelMixin,
							generics.GenericAPIView):
	serializer_class = DaySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly,)

	def create(self, request, *args, **kwargs):
		# SUPER IMPORTANT! CHECK FIRST THAT THE DAY HASN'T ALREADY BEEN SAVED IN THE DB.
		# THIS CHECK SHOULD PROBABLY DONE IN THE MODELS MODULE!!!!!!!!!
		serializer = DaySerializer(data=request.data)
		#serializer.initial_data['date'] = dateutil.parser.parse(serializer.initial_data['date'])
		values = {key: value for key, value in serializer.initial_data.items()}
		values['user'] = self.request.user
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def update(self, request, *args, **kwargs):
		#serializer = DaySerializer(data=request.data)
		#uuid = serializer.initial_data['uuid']
		values = {key: value for key, value in self.request.data.items()}
		dbEntry = Day.objects.get(uuid=values['uuid'])
		values['user'] = self.request.user.pk
		values['date'] = dbEntry.date
		serializer_values = dbEntry.getDict()
		serializer_values['user'] = self.request.user.pk
		serializer = DaySerializer(data=serializer_values)
		#values = {key: value for key, value in serializer.initial_data.items() if key != 'uuid'}
		#serializer.initial_data['date'] = dateutil.parser.parse(serializer.initial_data['date'])
		#serializer.initial_data['date'] = dbEntry.date
		#serializer.initial_data['user'] = self.request.user.pk
		serializer.is_valid(raise_exception=True)
		#values['user'] = request.user.pk
		#values['date'] = dbEntry.date
		newSerializer = DaySerializer(dbEntry, data=values)
		newSerializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

	def destroy(self, request, *args, **kwargs):
		data = DaySerializer(data=request.data)
		dbEntry = Day.objects.get(uuid=data.initial_data['uuid'])
		serializer = DaySerializer(data=dbEntry.getDict())
		serializer['user'] = self.request.user
		serializer.is_valid(raise_exception=True)
		self.perform_destroy(dbEntry)
		return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

'''
class InsertUpdateDeleteAPI(APIView):
	def post(self, request):
		serializer = DaySerializer(data=request.data)
		serializer.initial_data['date'] = dateutil.parser.parse(serializer.initial_data['date'])
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_RQUEST)

	def put(self, request):
		serializer = DaySerializer(data=request.data)
		dbEntry = Day.objects.get(uuid=serializer.initial_data['uuid'])
		serializer.initial_data['date'] = dateutil.parser.parse(serializer.initial_data['date'])
		values = {key: value for key, value in serializer.initial_data.items() if key != 'uuid'}
		newSerializer = DaySerializer(dbEntry, data=values)
		if newSerializer.is_valid():
			newSerializer.save()
			return Response(newSerializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request):
		data = DaySerializer(data=request.data)
		dbEntry = Day.objects.get(uuid=data.initial_data['uuid'])
		dbEntry.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

'''
#############################################################################

@require_http_methods(["GET"])
def getCalendarEntriesByYear(request, year):
	'''
	Returns all calendar entries for a given year. Only accepts get methods.
	If a different method is used in the request, returns a 405 status code. 
	'''
	queryset = Day.objects.filter(date__year=2016)
	data = {}
	for query in queryset:
		date = query.date
		date = '{}-{:02d}-{:02d}'.format(date.year, date.month, date.day)
		data[date] = {'id': query.pk,
		                    'sleepingQuality': query.sleepingQuality,
		                    'tirednessFeeling': query.tirednessFeeling,
		                    'userId': query.user.id,
		                    'date': str(query.date),
		                    'uuid': query.uuid}
	data = json.dumps(data)
	return JsonResponse(data)


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


class InsertUpdateDelete(View):
	http_method_names = ['post', 'put', 'delete']

	@csrf_exempt
	def post(self, request):
		items = dict(request.POST.items())
		date = getDatetimeFromISO(items['date'])
		user = User.objects.get(pk=items['userId'])
		newEntry = Day.objects.create(user=user,
			                date=date,
			                sleepingQuality=items['sleepingQuality'],
			                tirednessFeeling=items['tirednessFeeling'],
			                )
		
		responseData = Day.objects.get(uuid=newEntry.uuid)
		serializer = DaySerializer(responseData)
		#responseData = responseData.getDict()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						'responseData': serializer.data						
						}
		return JsonResponse(returnJson)

		'''
		data = JSONParser().parse(request)
		data = dict(request.POST.items())
		serializer = DaySerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
		'''

	def put(self, request):
		'''
		The request object cannot have a PUT attribute, so the data that comes in a  put request
		cannot be accessed by calling request.PUT. Instead, we need to access the body of the
		request and decode it from bytes into strings, and read its data with the json.loads function.
		We then convert this data into a Python dictionary. 
		'''
		inputData = dict(json.loads(request.body.decode()))
		#inputData = JSONParser().parse(request)
		entryUUID = inputData['UUID']
		dbEntry = Day.objects.get(uuid=entryUUID)
		dbEntry.sleepingQuality = inputData['sleepingQuality']
		dbEntry.tirednessFeeling = inputData['tirednessFeeling']
		dbEntry.date_modified = timezone.now()
		dbEntry.save()
		responseData = Day.objects.get(uuid=entryUUID)
		responseData = responseData.getDict()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						'responseData': responseData
						}
		return JsonResponse(returnJson)
		'''
		inputData = JSONParser().parse(request)
		entryUUID = inputData.get('UUID')
		dbEntry = Day.objects.get(uuid=entryUUID)
		serializer = DaySerializer(dbEntry, data=inputData)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
		'''
	def delete(self, request):
		'''
		The request object cannot have a DELETE attribute, so the data that comes in a  put request
		cannot be accessed by calling request.DELETE. Instead, we need to access the body of the
		request and decode it from bytes into strings, and read its data with the json.loads function.
		We then convert this data into a Python dictionary. 
		'''
		requestData = dict(json.loads(request.body.decode()))
		entryUUID = requestData['UUID']
		dbEntry = Day.objects.get(uuid=entryUUID)
		dbEntry.delete()
		returnJson = {
						'message': 'success',
						'status': 200,
						'token': '',
						}
		return JsonResponse(returnJson)



#######################################################################

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


