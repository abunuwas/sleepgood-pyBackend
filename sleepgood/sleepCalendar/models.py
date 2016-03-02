from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import uuid
import datetime


def generateUUID(userId, date):
	'''
	Returns an md5 hash using string which combines the user id plus the calendar date of the event
	as a way to generate a unique value. Not sure yet, though, if this is the best approach...
	'''
	currentMilliseconds = datetime.datetime.now().timestamp()
	uuidValue = uuid.uuid3(uuid.NAMESPACE_DNS, str(userId) + str(date) + str(currentMilliseconds))
	return str(uuidValue)


class Day(models.Model):
	good = 'good'
	bad = 'bad'
	regular = 'regular'
	choices = (
		(good, 'good'), 
		(bad, 'bad'), 
		(regular, 'regular')
		)
	sleepingQuality = models.CharField(max_length=7, choices=choices)
	tirednessFeeling = models.CharField(max_length=7, choices=choices)
	date = models.DateTimeField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	uuid = models.CharField(max_length=32)
	# Verify that auto_now_add and auto_now are actually the best choices for this
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('date_created',)

	def getDict(self):
		'''
		Some of the class attributes are instances of other classes, so they are not serializable into Json.
		This method provides a dictionary representation of all class' attributes for those cases in which
		they must be serialized.  
		'''
		return {'sleepingQuality': self.sleepingQuality,
		         'tirednessFeeling': self.tirednessFeeling,
		         'date': str(self.date),
		         'userId': str(self.user),
		         'date_created': str(self.date_created),
		         'date_modified': str(self.date_modified)
		         }

	def save(self, *args, **kwargs):
		uuid = generateUUID(self.user_id, self.date)
		self.uuid = str(uuid)
		super(Day, self).save(*args, **kwargs)

	def __str__(self):
		return 'Calendar(user={}, date={}, sleepingQuality={}, tirednessFeeling={}, uuid={})'.format(
			self.user, self.date, self.sleepingQuality, self.tirednessFeeling, self.uuid)



