from rest_framework import serializers
from .models import Day, User, Test


# # Serializers define the API representation
# class UserSerializer(serializers.ModelSerializer):
# 	days = serializers.PrimaryKeyRelatedField(many=True, queryset=Day.objects.all())
#
# 	class Meta:
# 		model = User
# 		fields = ('id', 'username', 'email', 'days')


class TestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Test
		fields = ('id', 'title', 'code', 'user')


class EntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Day
		fields = ('sleepingQuality', 'tirednessFeeling', 'date', 'user', 'uuid')


class DaySerializer(serializers.ModelSerializer):
	class Meta:
		model = Day
		fields = ('sleepingQuality', 'tirednessFeeling', 'date', 'uuid', 'user')
