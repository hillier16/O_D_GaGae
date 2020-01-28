from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import json
import datetime

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
        group_member = GroupMember.objects.get(group=Group.objects.get(pk=data['group_id']),
                                               member=User.objects.get(pk=uid))
        if group_member.is_alarm_on:
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
        notice = GroupNotice.objects.filter(group=request.GET.get('group_id')).order_by('-generated_date')[:1]
        serializer = groupNoticeViewSerializer(notice, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class groupNoticeView(APIView):
    def get(self, request, format=None):
        notice = GroupNotice.objects.filter(group=request.GET.get('group_id')).order_by('-generated_date')
        serializer = groupNoticeViewSerializer(notice, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_notice = GroupNotice(group=Group.objects.get(pk=data['group_id']), description=data['description'],
                                 author=User.objects.get(pk=uid))
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


class groupScheduleView(APIView):
    def get(self, request, format=None):
        schedule = GroupSchedule.objects.filter(group=Group.objects.get(pk=request.GET.get('group_id')))
        serializer = groupScheduleViewSerializer(schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_schedule = GroupSchedule(group=Group.objects.get(pk=data['group_id']), start_time=data['start_time'],
                                     end_time=data['end_time'], description=data['description'],
                                     author=User.objects.get(pk=uid))
        new_schedule.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        schedule = GroupSchedule.objects.get(pk=data['groupSchedule_id'])
        schedule.start_time = data['start_time']
        schedule.end_time = data['end_time']
        schedule.description = data['description']
        schedule.author = User.objects.get(pk=uid)
        schedule.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        schedule = GroupSchedule.objects.get(pk=request.GET.get('groupSchedule_id'))
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class groupBoardView(APIView):
    def get(self, request, format=None):
        serializer = GroupBoardViewSerializer(GroupBoard.objects.filter(group=request.GET.get('group_id')), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_group_board = GroupBoard(group=Group.objects.get(pk=data['group_id']), description=data['description'],
                                     due_date=data['due_date'])
        new_group_board.author = User.objects.get(pk=uid)
        new_group_board.save()

        p_list = data['person_in_charge']
        for p in p_list:
            new_group_board.person_in_charge.add(User.objects.get(uid=p))

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        groupboard = GroupBoard.objects.get(pk=data['groupBoard_id'])
        groupboard.description = data['description']
        groupboard.due_date = data['due_date']
        groupboard.author = User.objects.get(pk=uid)
        groupboard.save()

        groupboard.person_in_charge.clear()
        p_list = data['person_in_charge']
        for p in p_list:
            groupboard.person_in_charge.add(User.objects.get(uid=p))

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        groupboard = GroupBoard.objects.get(pk=request.GET.get('groupBoard_id'))
        groupboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class timeTableView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        serializer = TimeTableSerializer(TimeTable.objects.filter(owner=uid), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_timetable = TimeTable(owner=User.objects.get(pk=uid), title=data['title'], location=data['location'],
                                  start_time=data['start_time'], end_time=data['end_time'], day=data['day'])
        new_timetable.save();
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))
        timetable = TimeTable.objects.get(pk=data['timeTable_id'])
        timetable.title = data['title']
        timetable.location = data['location']
        timetable.day = data['day']
        timetable.start_time = data['start_time']
        timetable.end_time = data['end_time']
        timetable.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        timetable = TimeTable.objects.get(pk=request.GET.get('timeTable_id'))
        timetable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class personalScheduleView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        schedule = PersonalSchedule.objects.filter(owner=User.objects.get(pk=uid))
        serializer = personalScheduleViewSerializer(schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_schedule = PersonalSchedule(owner=User.objects.get(pk=uid), start_time=data['start_time'],
                                        end_time=data['end_time'], description=data['description'])
        new_schedule.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))
        schedule = PersonalSchedule.objects.get(pk=data['personalSchedule_id'])
        schedule.start_time = data['start_time']
        schedule.end_time = data['end_time']
        schedule.description = data['description']
        schedule.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        schedule = PersonalSchedule.objects.get(pk=request.GET.get('personalSchedule_id'))
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class surveyView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        user = User.objects.get(pk=uid)
        user_age_range = int(user.age) // 10
        survey = Survey.objects.filter(target_gender=user.gender, is_active=True,
                                        target_age_start__lte=user_age_range, target_age_end__gte=user_age_range).order_by('-edited_date')
        serializer = surveyViewSerializer(survey, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        uid = get_uid_from_jwt(request)
        data = json.loads(request.body.decode('utf-8'))
        new_survey = Survey(title=data['title'], author=User.objects.get(pk=uid), description=data['description'],
                            target_gender=data['target_gender'], target_age_start=data['target_age_start'], target_age_end=data['target_age_end'])
        new_survey.save()
        for question in data['question']:
            new_survey_question = SurveyQuestion(survey=new_survey, index=question['index'], content=question['content'], question_type=question['type'], choices=question['choices'])
            new_survey_question.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))
        survey = Survey.objects.get(pk=data['survey_id'])
        survey.is_active = False
        survey.save()
        return Response(status=status.HTTP_201_CREATED)


class mainSurveyView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        user = User.objects.get(pk=uid)
        user_age_range = int(user.age) // 10
        survey = Survey.objects.filter(target_gender=user.gender, is_active=True,
                                        target_age_start__lte=user_age_range, target_age_end__gte=user_age_range).order_by('-edited_date')[:8]
        serializer = surveyViewSerializer(survey, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class mySurveyView(APIView):
    def get(self, request, format=None):
        uid = get_uid_from_jwt(request)
        survey = Survey.objects.filter(author=User.objects.get(pk=uid)).order_by('-edited_date')
        serializer = surveyViewSerializer(survey, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class updateSurveyView(APIView):
    def put(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))
        survey = Survey.objects.get(pk=data['survey_id'])
        survey.edited_date = datetime.datetime.now()
        survey.save()
        return Response(status=status.HTTP_201_CREATED)
