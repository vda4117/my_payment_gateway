from rest_framework import serializers

from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CyberSourceTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = CyberSourceTransaction
		fields = '__all__'


class CyberSourceResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = CyberSourceResponse
		fields = '__all__'