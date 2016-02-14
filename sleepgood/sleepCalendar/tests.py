from django.test import TestCase, Client
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve
from django.utils import timezone

import datetime
import json

from .views import InsertUpdate, generateUUID, getDatetimeFromISO
from .models import Calendar


#### USE DECORATORS TO SPECIFY WHICH METHODS ARE ALLOWED IN EVERY VIEW


class insertCalendarEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

	def test_entries_inserted_correctly(self):
		data = {'_userId': '1',
				'sleepingQuality': 'good',
				'tirednessFeeling': 'bad',
				'date': '2016-02-09T23:48:14.297Z'
				}

		response = self.c.post('/1/calendar', data=data)

		event = Calendar.objects.all()

		self.assertEqual(len(event), 1)

	def test_wrong_method(self):
		response = self.c.get('/1/calendar')

		self.assertEqual(response.status_code, 405)


class updateCalendarEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

		userId = 1
		dateISO = '2016-02-09T23:48:14.297Z'
		date = getDatetimeFromISO(dateISO)
		generateUUID(str(userId), str(date))
		entryUUID = generateUUID(str(userId), str(date))
		setUpEntry = Calendar(userId=1,
			                  sleepingQuality='bad',
			                  tirednessFeeling='good',
			                  date=date,
			                  uuid=entryUUID,
			                  date_created=timezone.now(),
			                  date_modified=timezone.now())
		setUpEntry.save()
		self.setUpEntry = Calendar.objects.get(uuid=entryUUID)

	def test_update_calendar_entry(self):
		request = HttpRequest()
		data = {'_userId': 1,
				'sleepingQuality': 'good',
				'tirednessFeeling': 'bad',
				'date': '2016-02-09T23:48:14.297Z',
				'UUID': self.setUpEntry.uuid		        
				}
		dataJSON = json.dumps(data)
		response = self.c.put('/1/calendar',
			        content_type='application/json',
			        data=dataJSON)
		
		dbEntry = Calendar.objects.get(uuid=self.setUpEntry.uuid)
		self.assertEqual(dbEntry.sleepingQuality, 'good')
		self.assertEqual(dbEntry.tirednessFeeling, 'bad')





