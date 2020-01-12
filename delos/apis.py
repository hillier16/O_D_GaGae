from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

import json
from .models import *
from .serializers import *
from .utils import *


class getUserGroup(APIView):
    def get_object(self, uid):
        try:
            group_list = GroupMember.objects.filter(member=uid).values_list('group')
            group = Group.objects.filter(pk__in = group_list).values('id', 'name', 'description', 'code', 'member_num')
            return group
        except (GroupMember.DoesNotExist, Group.DoesNotExist):
            raise Http404

    def get(self, request):
        uid = get_uid_from_jwt(request)
        groups = self.get_object(uid)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class createGroup(APIView):
    def is_code_duplicate(self, code):
        exist = Group.objects.filter(code=code)
        if exist.count() == 0:
            return False
        return True

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        serializer = GroupSerializer(data=request.data)
        # print(request.data.get('name'))
        # new_group = Group(name=json.loads(request.body.decode("utf-8"))['name'], description=json.loads(request.body.decode("utf-8"))['description'], code="ABC")
        # new_group.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        name = "new group"
        description = "this is new group"
        uid = get_uid_from_jwt(request)
        code = make_random_group_code()
        while(self.is_code_duplicate(code)):
            code = make_random_group_code()
        new_group = Group(name=name, description=description, code=code)
        new_group.save()
        return Response(status=status.HTTP_201_CREATED)