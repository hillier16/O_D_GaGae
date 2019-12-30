from rest_framework import serializers
from .models import *


class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'