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
from .serializers import UserSerializer, GroupSerializer, DaySerializer, EntrySerializer
from .permissions import IsOwnerOrReadOnly


def indexView(request):
	return HttpResponse('You are in index view!')

#######################################################################


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
		print(userId);
		# Filter data by user and year. Maybe this should be modified later on... 
		queryset = Day.objects.filter(user=userId, date__year=year)
		serializer = self.get_serializer(queryset, many=True)
		return_data = {}
		for result in serializer.data:
			# Take the date year-month-day data from the ISO structure
			# to use it as a key for the data related to this date in the 
			# JSON. 
			date = result['date'][:10]
			return_data[date] = result	    
		return Response(return_data)

	def get(self, request, *args, **kwargs):
		result_set = self.list(request, *args, **kwargs)
		return result_set

class GetCalendarEntry(mixins.ListModelMixin,
						generics.GenericAPIView):
	queryset = Day.objects.all()
	lookup_field = 'uuid'
	serializer_class = EntrySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly,)

	def get(self, request, *args, **kwargs):
		uuid = kwargs['uuid']
		user = request.user
		userId = user.id
		queryset = Day.objects.filter(user=userId, uuid=uuid)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

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
		values = {key: value for key, value in request.data.items()}
		values['user'] = self.request.user.pk
		serializer = DaySerializer(data=values)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		# Override this method passing user data to the save method, which will signed
		# the current user as owner of this data. 
		serializer.save(user=self.request.user)

	def update(self, request, *args, **kwargs):
		'''
		It updates a value in the database. Data can only be modified by users who own/created it. 
		This method extensively overrides the original update method from the UpdateModelMixin class. 
		It expects the following parameters from the request:
		<uuid>
		<tirednessFeeling>
		<sleepingQuality>
		User data must be included in the headers. 
		'''
		# Create dictionary of values from payload in the request. 
		# The `values` dictionary stores data that will be used to build a
		# serializer with which we can updated the corresponding database entry. 
		values = {key: value for key, value in self.request.data.items()}
		# Obtain the primary key of the user object returned by the request. 
		values['user'] = self.request.user.pk
		# Retrieve database entry corresponding to the uuid value included in the request. 
		dbEntry = Day.objects.get(uuid=values['uuid'])
		# Include the date field from the database entry in the values dictioanry. 		
		values['date'] = dbEntry.date
		# Build a dictionary of values for the serializer object from the database entry. 
		serializer_values = dbEntry.getDict()
		# Add the primary of hte user to the dictionary of values for the seriazlier. 
		serializer_values['user'] = self.request.user.pk
		# Build the serializer object. This object represents the old database entry
		# that will be updated. 
		serializer = DaySerializer(data=serializer_values)
		# Validate data in the serializer to be able to save it. 
		serializer.is_valid(raise_exception=True)
		# Build new serializer from the new values included in the request. 
		newSerializer = DaySerializer(dbEntry, data=values)
		# Validate data for the new serializer object. 
		newSerializer.is_valid(raise_exception=True)
		# Update database entry. 
		self.perform_update(newSerializer)
		return Response(newSerializer.data)

	def destroy(self, request, *args, **kwargs):
		dbEntry = Day.objects.get(uuid=request.data.get('uuid'))
		return_data = dbEntry.getDict()
		return_data = json.dumps(return_data)
		self.perform_destroy(dbEntry)
		return Response(return_data)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)



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


