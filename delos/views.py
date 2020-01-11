from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
import requests
import json

from .models import *
from .serializers import *


headers = {}


# Create your views here.
def home(request):
    return render(request, 'delos/home.html', {})


def login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/oauth'

    url = 'https://kauth.kakao.com/oauth/authorize?'
    url += 'client_id=' + client_id
    url += '&redirect_uri=' + redirect_uri
    url += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    print("login_request_uri = " + url)
    return redirect(url)


def unlink(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/withdraw'

    url = 'https://kauth.kakao.com/oauth/authorize?'
    url += 'client_id=' + client_id
    url += '&redirect_uri=' + redirect_uri
    url += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    print("login_request_uri = " + url)
    return redirect(url)


def oauth(request):
    code = request.GET['code']
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    url = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    url += "client_id=" + client_id
    url += "&redirect_uri=" + redirect_uri
    url += "&code=" + code

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    access_token_request_uri_data = requests.get(url, headers=headers)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    print(access_token)

    url = "https://kapi.kakao.com/v1/user/signup"
    headers.update({'Authorization': "Bearer " + str(access_token)})
    response = requests.request("POST", url, headers=headers)
    print(response.text)

    url = "https://kapi.kakao.com/v2/user/me"
    params = 'property_keys=["properties.nickname"]'
    response = requests.request("POST", url, headers=headers, data=params)
    print(response.text)

    json_data = response.json()
    properties = json_data['properties']
    user, flag = User.objects.get_or_create(uid=json_data['id'], name=properties['nickname'])

    return render(request, 'delos/home.html', {})


def withdraw(request):
    code = request.GET['code']
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    url = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    url += "client_id=" + client_id
    url += "&redirect_uri=" + redirect_uri
    url += "&code=" + code
    print(code)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    access_token_request_uri_data = requests.get(url, headers=headers)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    print(access_token)

    url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {'Authorization': "Bearer " + str(access_token)}
    response = requests.request("POST", url, headers=headers)
    print(response.text)
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


class getUserGroup(APIView):
    def get_object(self, uid):
        try:
            group_list = GroupMember.objects.filter(member=uid).values('group')
            group = Group.objects.filter(pk__in = group_list).values('id', 'name', 'description', 'code', 'member_num')
            return group
        except (GroupMember.DoesNotExist, Group.DoesNotExist):
            raise Http404

    def get(self, request, uid):
        groups = self.get_object(uid)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)