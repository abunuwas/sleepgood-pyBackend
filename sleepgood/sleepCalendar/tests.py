from django.test import TestCase, Client
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import datetime
import json

from .views import InsertUpdateDelete, getDatetimeFromISO
from .models import Day
from .serializers import DaySerializer


class GetDayEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

		carlos = User.objects.create(username='carlos')

		dateISO = '2016-02-09T23:48:14.297Z'
		date = getDatetimeFromISO(dateISO)
		setUpEntry = Day.objects.create(user=carlos,
			                  sleepingQuality='bad',
			                  tirednessFeeling='good',
			                  date=date,
			                  )
		self.setUpEntry = Day.objects.get(date=date)

	def test_retrieve_entries(self):
		response = self.c.get('/calendar/year/2016')
		self.assertEqual(response.status_code, 200)

	def test_retrieve_wrong_method(self):
		response = self.c.post('/calendar/year/2016')
		self.assertEqual(response.status_code, 405)	


class InsertDayEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

		carlos = User.objects.create(username='carlos')

	def test_entries_inserted_correctly(self):
		data = {'_userId': '1',
				'sleepingQuality': 'good',
				'tirednessFeeling': 'bad',
				'date': '2016-02-09T23:48:14.297Z'
				}

		response = self.c.post('/calendar', data=data)

		event = Day.objects.all()

		self.assertEqual(len(event), 1)

	def test_wrong_method(self):
		response = self.c.get('/calendar')
		self.assertEqual(response.status_code, 405)


class UpdateDayEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

		carlos = User.objects.create(username='carlos')

		dateISO = '2016-02-09T23:48:14.297Z'
		date = getDatetimeFromISO(dateISO)
		setUpEntry = Day.objects.create(user=carlos,
			                  sleepingQuality='bad',
			                  tirednessFeeling='good',
			                  date=date
			                  )
		self.setUpEntry = Day.objects.get(date=date)
		print('In setUp ', self.setUpEntry)

	def test_update_day_entry(self):
		data = {'_userId': 1,
				'sleepingQuality': 'good',
				'tirednessFeeling': 'bad',
				'date': '2016-02-09T23:48:14.297Z',
				'UUID': self.setUpEntry.uuid		        
				}
		entry = Day.objects.get(uuid=self.setUpEntry.uuid)
		print('Testing... ', entry)
		dataJSON = json.dumps(data)
		response = self.c.put('/calendar',
			        content_type='application/json',
			        data=dataJSON)

		dbEntry = Day.objects.get(uuid=self.setUpEntry.uuid)
		self.assertEqual(dbEntry.sleepingQuality, 'good')
		self.assertEqual(dbEntry.tirednessFeeling, 'bad')

class DeleteDayEntry(TestCase):

	def setUp(self):
		self.c = Client()

		carlos = User.objects.create(username='carlos')

		dateISO = '2016-02-09T23:48:14.297Z'
		date = getDatetimeFromISO(dateISO)
		setUpEntry = Day.objects.create(user=carlos,
			                  sleepingQuality='bad',
			                  tirednessFeeling='good',
			                  date=date
			                  )
		self.setUpEntry = Day.objects.get(date=date)

	def test_delete_day_entry(self):
		request = HttpRequest()
		data = {'_userId': 1,
				'UUID': self.setUpEntry.uuid		        
				}
		dataJSON = json.dumps(data)
		response = self.c.delete('/calendar',
			        content_type='application/json',
			        data=dataJSON)
		
		self.assertEqual(len(Day.objects.all()), 0)

class TestSerializers(TestCase):

	def setUp(self):
		carlos = User.objects.create(username='carlos', email='j@j.com')
		self.day = Day(sleepingQuality='bad', tirednessFeeling='good', date=timezone.now(), user=carlos)

	def test_serializer_day(self):
		serializer = DaySerializer(self.day)
		print(serializer.data)






