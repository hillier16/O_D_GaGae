from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from calendar import timegm
from datetime import datetime
import requests

from .serializers import UserSerializer
from . models import User



headers = {}


def login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/api/oauth'

    url = 'https://kauth.kakao.com/oauth/authorize?'
    url += 'client_id=' + client_id
    url += '&redirect_uri=' + redirect_uri
    url += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    print("login_request_uri = " + url)
    return redirect(url)


'''
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
'''

def unlink(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/api/withdraw'

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
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/api/oauth'

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

    user, flag = User.objects.get_or_create(uid=json_data['id'])
    if flag:
        user.name = properties['nickname'],
        user.password = make_password(settings.SECRET_PASSWORD)
        user.save()
    token = obtain_jwt_token(user)
    print(token)
    userserial = UserSerializer(user)

    response = HttpResponse(userserial)
    response['token'] = token
    response['Content-Type'] = 'application/json'
    print("JWT token = " + token)
    return response


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
    user = User.objects.get(uid="1247257827")
    user.delete()
    return redirect('home')


def obtain_jwt_token(user: User):
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    return jwt_encode_handler(payload)


class loginKakaoView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        access_token = request.META.get('HTTP_KAKAO_ACCESS_TOKEN')

        url = "https://kapi.kakao.com/v1/user/signup"
        headers.update({'Authorization': "Bearer " + str(access_token)})
        response = requests.request("POST", url, headers=headers)
        print(response.text)

        url = "https://kapi.kakao.com/v2/user/me"
        params = 'property_keys=["properties.nickname"]'
        response = requests.request("POST", url, headers=headers, data=params)
        print(response.text)

        json_data = response.json()
        user, flag = User.objects.get_or_create(uid=json_data['id'])

        properties = json_data['properties']
        if flag:
            user.name = properties['nickname'],
            user.password = make_password(settings.SECRET_PASSWORD)
            user.save()

        token = obtain_jwt_token(user)
        userserial = UserSerializer(user)
        response = Response(userserial.data, status=status.HTTP_201_CREATED)
        response['authorization'] = "JWT " + token
        response['Content-Type'] = 'application/json'
        print("JWT = " + token)
        return response
