# from django.test import TestCase
import requests

# Create your tests here.


url = 'http://localhost:8000/api/loginKakao'


headers = {'Content-Type': 'application/json',
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTI0NzI1NzgyNyIsInVzZXJuYW1lIjoiMTI0NzI1NzgyNyIsImV4cCI6MTU4MDk5ODAyMywidWlkIjoiMTI0NzI1NzgyNyIsIm9yaWdfaWF0IjoxNTgwMzkzMjIzfQ.TRf92cZ2WfF-oZ9eCb6dskATnELa_UP75bYxSuBVvi0'}

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