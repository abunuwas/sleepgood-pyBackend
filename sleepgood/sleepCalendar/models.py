from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
	sleepingQuality = models.CharField(max_length=7)
	tirednessFeeling = models.CharField(max_length=7)
	date = models.DateTimeField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# Provisional field ofr user id until the model for user is implemented
	#userId = models.IntegerField()
	uuid = models.CharField(max_length=32) # verify that certainly 32 is the max length of an md5 hash
	date_created = models.DateTimeField()
	date_modified = models.DateTimeField()

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

