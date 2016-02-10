from django.test import TestCase, Client
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve

import datetime
import json

from .views import insertCalendarEntry, generateUUID, getDate, getYearMonthDayFromISO, updateCalendarEntry
from .models import Calendar


#### USE DECORATORS TO SPECIFY WHICH METHODS ARE ALLOWED IN EVERY VIEW


class insertCalendarEntryTest(TestCase):

	def test_entries_inserted_correctly(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['_userId'] = '1'
		request.POST['sleepingQuality'] = 'Good'
		request.POST['tirednessFeeling'] = 'Bad'
		request.POST['date'] = '2016-02-09T23:48:14.297Z'

		request_elements = dict(request.POST.items())

		response = insertCalendarEntry(request, 1)

		event = Calendar.objects.all()

		self.assertEqual(response.status_code, 302)
		self.assertEqual(len(event), 1)


class updateCalendarEntryTest(TestCase):

	def setUp(self):
		self.c = Client()

		userId = 1
		dateISO = '2016-02-09T23:48:14.297Z'
		dateString = getYearMonthDayFromISO(dateISO)
		date = getDate(dateISO)
		generateUUID(str(userId), dateString)
		entryUUID = generateUUID(str(userId), dateString)
		setUpEntry = Calendar(userId=1,
			                  sleepingQuality='bad',
			                  tirednessFeeling='good',
			                  date=date,
			                  uuid=entryUUID)
		setUpEntry.save()
		self.setUpEntry = Calendar.objects.get(uuid=entryUUID)

	def test_url_redirect_update(self):
		response = self.c.put('/1/calendar',
			        content_type='application/json',
			        data='')		
		self.assertEqual(response['Location'], '/1/calendar/update')
		self.assertEqual(response.status_code, 302)

	def test_update_calendar_entry(self):
		request = HttpRequest()
		data = {'_userId': 1,
				'sleepingQuality': 'Good',
				'tirednessFeeling': 'Bad',
				'date': '2016-02-09T23:48:14.297Z',
				'UUID': self.setUpEntry.uuid		        
				}
		dataJSON = json.dumps(data)
		response = self.c.put('/1/calendar/update',
			        content_type='application/json',
			        data=dataJSON)
		print(response.content)




