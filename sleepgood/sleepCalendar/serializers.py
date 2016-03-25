from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Day


# Serializers define the API representation
class UserSerializer(serializers.HyperlinkedModelSerializer):
	days = serializers.StringRelatedField()

	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'is_staff', 'days')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')


class DaySerializer(serializers.ModelSerializer):
	#user = serializers.PrimaryKeyRelatedField(read_only=True)
	#pk = serializers.IntegerField(read_only=True)
	#sleepingQuality = serializers.CharField(max_length=7)
	#tirednessFeeling = serializers.CharField(max_length=7)
	#date = serializers.DateTimeField()
	#uuid = serializers.CharField(max_length=32)
	#date_created = serializers.DateTimeField()
	#date_modified = serializers.DateTimeField()
	#user = serializers.StringRelatedField()

	class Meta:
		model = Day
		fields = ('sleepingQuality', 'tirednessFeeling', 'date', 
			'user', 'uuid')

	def create(self, validated_data):
		'''
		Create and return a new 'Day' instance, given the validated data.
		'''
		return Day.objects.create(**validated_data)

	"""
	def update(self, instance, validated_data):
		'''
		Update and return an existing 'Day' instance, given validated data.
		'''
		instance.sleepingQuality = validated_data.get('sleepingQuality', instance.sleepingQuality)
		instance.tirednessFeeling = validated_data.get('tirednessFeeling', instance.tirednessFeeling)
		instance.date = validated_data.get('date', instance.date)
		instance.user = validated_data.get('user', instance.user)
		instance.save()
		return instance
	"""
