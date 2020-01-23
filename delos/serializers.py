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

###########################################################################

# groupView
class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'code', 'member_num')
class groupViewSerializer(serializers.ModelSerializer):
    group = GroupDetailSerializer()
    class Meta:
        model = GroupMember
        fields = ('group', 'is_alarm_on')


# groupMemberView
class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name')
class groupMemberViewSerializer(serializers.ModelSerializer):
    member = UserNameSerializer()
    class Meta:
        model = GroupMember
        fields = ('member', 'joined_date')


# groupNoticeView
class groupNoticeViewSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()
    class Meta:
        model = GroupNotice
        fields = ('id', 'description', 'generated_date', 'author')