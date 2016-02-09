from django.db import models

class Calendar(models.Model):
	sleepingQuality = models.CharField(max_length=7)
	tirednessFeeling = models.CharField(max_length=7)
	date = models.DateTimeField()
	#year = models.IntegerField()
	#month = models.IntegerField()
	#day = models.IntegerField()
	#userId = models.ForeignKey(User, on_delete=models.CASCADE)
	# Provisional field ofr user id until the model for user is implemented
	userId = models.IntegerField()
	uuid = models.CharField(max_length=32) # verify that certainly 32 is the max length of an md5 hash
	date_created = models.DateTimeField()
	date_modified = models.DateTimeField()

	def __str__(self):
		return 'Calendar(user={}, date={}, sleepingQuality={}, tirednessFeeling={}, uuid={}'.format(
			self.userId, self.date, self.sleepingQuality, self.tirednessFeeling, self.uuid)
