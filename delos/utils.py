import string
import random
import datetime, time
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

string_pool = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
def make_random_group_code():
    code = ""
    for _ in range(6):
        code += random.choice(string_pool)
    return code


def get_uid_from_jwt(request):
    auth = JSONWebTokenAuthentication()
    jwt_value = auth.get_jwt_value(request)
    payload = api_settings.JWT_DECODE_HANDLER(jwt_value)
    return payload['user_id']


def filter_available_team_timetable(timetable_list, day, result_json):
    end_time = datetime.time(0)
    start_time = datetime.time(23, 59, 59)

    for i in range(len(timetable_list)):
        if i is 0:  # 첫시간
            start_time = timetable_list[i]['start_time']
            result = {}
            result["day"] = day
            result["start_time"] = end_time.strftime('%H:%M:00')
            result["end_time"] = start_time.strftime('%H:%M:00')
            result_json.append(result)

        if i == len(timetable_list) - 1:  # 마지막 시간
            end_time = timetable_list[i]['end_time']
            start_time = datetime.time(23, 59, 59)
            result = {}
            result["day"] = day
            result["start_time"] = end_time.strftime('%H:%M:00')
            result["end_time"] = start_time.strftime('%H:%M:00')
            result_json.append(result)
            break

        end_time = timetable_list[i]['end_time']
        start_time = timetable_list[i + 1]['start_time']
        if end_time < start_time:
            result = {}
            result["day"] = day
            result["start_time"] = end_time.strftime('%H:%M:00')
            result["end_time"] = start_time.strftime('%H:%M:00')
            result_json.append(result)

    if len(timetable_list) == 0:
        result = {}
        result["day"] = day
        result["start_time"] = end_time.strftime('%H:%M:00')
        result["end_time"] = start_time.strftime('%H:%M:00')
        result_json.append(result)
