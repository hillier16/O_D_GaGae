import string
import random

def get_uid_from_jwt(request):
    uid = 'user1'

    return uid


string_pool = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
def make_random_group_code():
    code = ""
    for _ in range(6):
        code += random.choice(string_pool)
    return code