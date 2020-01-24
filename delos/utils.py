import string
import random
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