from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests

from .models import *
from .serializers import *


headers = {}


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
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://' + settings.HOST_IP + '/oauth'

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