from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
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

	def __str__(self):
		return 'Calendar(user={}, date={}, sleepingQuality={}, tirednessFeeling={}, uuid={})'.format(
			self.user, self.date, self.sleepingQuality, self.tirednessFeeling, self.uuid)

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

