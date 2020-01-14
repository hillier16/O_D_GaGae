from delos.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'gender', 'age', 'survey_coin', 'joined_date')


class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'


class GroupScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSchedule
        fields = '__all__'


class GroupNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupNotice
        fields = '__all__'


class GroupBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBoard
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = '__all__'


