# from django.test import TestCase
import requests

# Create your tests here.


url = 'http://localhost:8000/api/loginKakao'


headers = {'Content-Type': 'application/json',
            'Authorization': 'JWT '}

#   get
def get():
    url_param = url + ''
    data = {'member': ['1', '2', '3']}
    response = requests.get(url_param, json=data, headers=headers)
    print(response.text)
    assert response.status_code == 200


#   post
def post():
    headers = {'kakao-access-token': "tooken"}
    response = requests.post(url, headers=headers)
    print(response.text)
    assert response.status_code == 201


#   put
def put():
    data = {'groupBoard_id': '5',
            'description': '해야할일321',
            'due_date': '2020-12-12T12:00:00',
            'person_in_charge' : [
                {'person': 'aweek43'}
            ]
    }
    response = requests.put(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201


#   delete
def delete():
    url_param = url + '?personalSchedule_id=1'
    response = requests.delete(url_param, headers=headers)
    # print(response.text)
    assert response.status_code == 204

post()
