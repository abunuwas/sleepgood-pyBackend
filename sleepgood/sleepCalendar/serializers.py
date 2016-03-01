from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Calendar


# Serializers define the API representation
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')


class CalendarSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	sleepingQuality = serializers.CharField(max_length=7)
	tirednessFeeling = serializers.CharField(max_length=7)
	date = serializers.DateTimeField()
	#user = serializers.ForeignKey(User, on_delete=models.CASCADE)
	uuid = serializers.CharField(max_length=32) 


