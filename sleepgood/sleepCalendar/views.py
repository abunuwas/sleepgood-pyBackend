import json
import dateutil.parser

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status, mixins, generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from six import BytesIO

from .jwtWrapper import jwtWrapper
from .models import Day
from .serializers import DaySerializer, EntrySerializer, TestSerializer


# Default


def indexView(request):
	return HttpResponse('You are in index view!')


# Calendar


class CalendarList(mixins.ListModelMixin,
				   generics.GenericAPIView):
	queryset = Day.objects.all()
	lookup_field = 'date__year'
	serializer_class = DaySerializer
	permission_classes = (permissions.AllowAny,)

	def list(self, request, *args, **kwargs):
		year = kwargs['date__year']

		# token validation
		wrapper = jwtWrapper()
		if 'HTTP_AUTHORIZATION' not in request.META:
			return Response('No authorization header', status=status.HTTP_401_UNAUTHORIZED)
		try:
			token = wrapper.check(request.META['HTTP_AUTHORIZATION']);
		except RuntimeError:
			return Response('error on token parsing.', status=status.HTTP_400_BAD_REQUEST)

		user_id = token['sub']
		# end token validation

		queryset = Day.objects.filter(user=user_id, date__year=year)
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


class CalendarDetails(mixins.RetrieveModelMixin,
					  mixins.CreateModelMixin,
					  mixins.UpdateModelMixin,
					  mixins.DestroyModelMixin,
					  generics.GenericAPIView):
	queryset = Day.objects.all()
	lookup_field = 'uuid'
	serializer_class = DaySerializer
	permission_classes = (permissions.AllowAny,)

	def get(self, request, *args, **kwargs):
		uuid = kwargs['uuid']
		user = request.user

		# token validation
		wrapper = jwtWrapper()
		if 'HTTP_AUTHORIZATION' not in request.META:
			return Response('No authorization header', status=status.HTTP_401_UNAUTHORIZED)
		try:
			token = wrapper.check(request.META['HTTP_AUTHORIZATION']);
		except RuntimeError:
			return Response('error on token parsing.', status=status.HTTP_400_BAD_REQUEST)

		user_id = token['sub']
		# end token validation

		queryset = Day.objects.filter(user=user_id, uuid=uuid)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):

		# token validation
		wrapper = jwtWrapper()
		if 'HTTP_AUTHORIZATION' not in request.META:
			return Response('No authorization header', status=status.HTTP_401_UNAUTHORIZED)
		try:
			token = wrapper.check(request.META['HTTP_AUTHORIZATION']);
		except RuntimeError:
			return Response('error on token parsing.', status=status.HTTP_400_BAD_REQUEST)

		user_id = token['sub']
		# end token validation

		values = {key: value for key, value in request.data.items()}
		values['user'] = user_id  # set user
		if not values:
			return Response('request payload is empty!.', status=status.HTTP_400_BAD_REQUEST)
		serializer = DaySerializer(data=values)

		date = dateutil.parser.parse(values['date']);
		print(type(date))
		queryset = Day.objects.filter(user=values['user'], date=date)
		if queryset:
			return Response('day already in database', status=status.HTTP_400_BAD_REQUEST)
		if serializer.is_valid():
			serializer.save()
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
