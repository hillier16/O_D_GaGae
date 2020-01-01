from django.shortcuts import render

from rest_framework import viewsets

from .models import *
from .serializers import *

# Create your views here.
def home(request):
    return render(request, 'delos/home.html', {})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersonalScheduleViewSet(viewsets.ModelViewSet):
    queryset = PersonalSchedule.objects.all()
    serializer_class = PersonalScheduleSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer


class GroupScheduleViewSet(viewsets.ModelViewSet):
    queryset = GroupSchedule.objects.all()
    serializer_class = GroupScheduleSerializer


class GroupNoticeViewSet(viewsets.ModelViewSet):
    queryset = GroupNotice.objects.all()
    serializer_class = GroupNoticeSerializer


class GroupBoardViewSet(viewsets.ModelViewSet):
    queryset = GroupBoard.objects.all()
    serializer_class = GroupBoardSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer


class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer


