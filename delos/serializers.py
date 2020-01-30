from delos.models import *
from rest_framework import serializers


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


# loginKakaoView
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'gender', 'age', 'survey_coin', 'joined_date')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name')
        

# groupView
class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'code', 'member_num')


# groupView
class GroupViewSerializer(serializers.ModelSerializer):
    group = GroupDetailSerializer()

    class Meta:
        model = GroupMember
        fields = ('group', 'is_alarm_on')


# groupMemberView
class GroupMemberViewSerializer(serializers.ModelSerializer):
    member = UserNameSerializer()

    class Meta:
        model = GroupMember
        fields = ('member', 'joined_date')


# groupNoticeView
class GroupNoticeViewSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()

    class Meta:
        model = GroupNotice
        fields = ('id', 'description', 'generated_date', 'author')


# groupScheduleView
class GroupScheduleViewSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()

    class Meta:
        model = GroupSchedule
        fields = ('id', 'start_time', 'end_time', 'description', 'author')


# groupBoardView
class GroupBoardViewSerializer(serializers.ModelSerializer):
    person_in_charge = UserNameSerializer(many=True)

    class Meta:
        model = GroupBoard
        fields = ('id', 'description', 'due_date', 'author', 'person_in_charge')


# TimeTableView
class TimeTableViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ('title', 'location', 'day', 'start_time', 'end_time')


# personalScheduleView
class PersonalScheduleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = ('id', 'start_time', 'end_time', 'description')

        
# surveyView
class SurveyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'title', 'description')


# surveyAnswerView
class UserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'age')


# surveyAnswerView
class SurveyQuestionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ('id', 'index', 'content', 'question_type')


# surveyAnswerView
class SurveyAnswerViewSerializer(serializers.ModelSerializer):
    survey_question = SurveyQuestionViewSerializer()
    author = UserSurveySerializer()

    class Meta:
        model = SurveyAnswer
        fields = ('id', 'survey_question', 'content', 'author')


# groupBoardChargedView
class GroupBoardChargedViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBoard
        fields = ('id', 'group', 'description', 'due_date')