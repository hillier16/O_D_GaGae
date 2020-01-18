from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, QueryDict
import json

from .models import *
from .serializers import *
from .utils import *

from django.db import connection

class getUserGroup(APIView):
    def get_groups(self, uid):
        try:
            group = GroupMember.objects.filter(member=uid)
            return group
        except GroupMember.DoesNotExist:
            raise Http404

    def get(self, request):
        uid = get_uid_from_jwt(request)
        groups = self.get_groups(uid)
        serializer = getUserGroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class createGroup(APIView):
    def is_code_duplicate(self, code):
        exist = Group.objects.filter(code=code)
        if exist.count() == 0:
            return False
        return True

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        code = make_random_group_code()
        while(self.is_code_duplicate(code)):
            code = make_random_group_code()
        data = json.loads(request.body.decode('utf-8'))
        new_group = Group(name=data['name'], description=data['description'], code=code)
        new_group.save()
        GroupMember(group=new_group, member=User.objects.get(pk=uid)).save()
        return Response(code, status=status.HTTP_201_CREATED)


class joinGroup(APIView):
    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        group = Group.objects.get(code=data['code'])
        group.member_num += 1
        group.save()
        GroupMember(group=group, member=User.objects.get(pk=uid)).save()
        return Response(status=status.HTTP_201_CREATED)


class deleteGroup(APIView):
    def delete(self, request, format=None):
        uid = get_uid_from_jwt(request)
        group = Group.objects.get(pk=request.GET.get('group_id'))
        GroupMember.objects.get(group=group, member=User.objects.get(pk=uid)).delete()
        if group.member_num == 1:
            group.delete()
        else:
            group.member_num -= 1
            group.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class changeGroupAlarm(APIView):
    def put(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        group_member = GroupMember.objects.get(group=Group.objects.get(pk=data['group_id']), member=User.objects.get(pk=uid))
        if group_member.is_alarm_on == True:
            group_member.is_alarm_on = False
        else:
            group_member.is_alarm_on = True
        group_member.save()
        return Response(status=status.HTTP_201_CREATED)


class getGroupMember(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        serializer = getGroupMemberSerializer(GroupMember.objects.filter(group=request.GET.get('group_id')), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)