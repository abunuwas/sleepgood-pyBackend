from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve

import datetime

from .views import insertCalendarEntry
from .models import Calendar


class insertCalendarEntryTest(TestCase):

	def test_entries_inserted_correctly(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['_userId'] = '1'
		request.POST['sleepingQuality'] = 'Good'
		request.POST['tirednessFeeling'] = 'Bad'
		request.POST['_userId'] = '1'
		request.POST['date'] = '2016-02-09T23:48:14.297Z'

		request_elements = dict(request.POST.items())

		response = insertCalendarEntry(request, 1)

		event = Calendar.objects.all()

		self.assertEqual(response.status_code, 302)
		self.assertEqual(len(event), 1)



