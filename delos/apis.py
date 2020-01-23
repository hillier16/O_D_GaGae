from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import json

from .models import *
from .serializers import *
from .utils import *

class groupView(APIView):
    def get_groups(self, uid):
        try:
            group = GroupMember.objects.filter(member=uid)
            return group
        except GroupMember.DoesNotExist:
            raise Http404
    
    def is_code_duplicate(self, code):
        exist = Group.objects.filter(code=code)
        if exist.count() == 0:
            return False
        return True

    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        groups = self.get_groups(uid)
        serializer = groupViewSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        code = make_random_group_code()
        while(self.is_code_duplicate(code)):
            code = make_random_group_code()
        data = json.loads(request.body.decode('utf-8'))
        new_group = Group(name=data['name'], description=data['description'], code=code)
        new_group.save()
        GroupMember(group=new_group, member=User.objects.get(pk=uid)).save()
        response_body = {
            "code": code
        }
        return Response(response_body, status=status.HTTP_201_CREATED)


class groupMemberView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        member = GroupMember.objects.filter(group=request.GET.get('group_id'))
        serializer = groupMemberViewSerializer(member, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        group = Group.objects.get(code=data['code'])
        group.member_num += 1
        group.save()
        GroupMember(group=group, member=User.objects.get(pk=uid)).save()
        return Response(status=status.HTTP_201_CREATED)

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


class latestGroupNoticeView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        notice = GroupNotice.objects.filter(group=request.GET.get('group_id')).order_by('-generated_date')[:1]
        serializer = groupNoticeViewSerializer(notice, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class groupNoticeView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        notice = GroupNotice.objects.filter(group=request.GET.get('group_id')).order_by('-generated_date')
        serializer = groupNoticeViewSerializer(notice, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_notice = GroupNotice(group=Group.objects.get(pk=data['group_id']), description=data['description'], author=User.objects.get(pk=uid))
        new_notice.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        notice = GroupNotice.objects.get(pk=data['groupNotice_id'])
        if str(notice.author) != str(uid):
            return Response(status=status.HTTP_403_FORBIDDEN)
        notice.description = data['description']
        notice.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        uid = get_uid_from_jwt(request)
        notice = GroupNotice.objects.get(pk=request.GET.get('groupNotice_id'))
        if str(notice.author) != str(uid):
            return Response(status=status.HTTP_403_FORBIDDEN)
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)