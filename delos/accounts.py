from django.shortcuts import render, redirect, get_object_or_404
from calendar import timegm
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import requests
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.renderers import JSONRenderer


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