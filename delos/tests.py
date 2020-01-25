# from django.test import TestCase
import requests

# Create your tests here.
url = 'http://localhost:8000/api/personalSchedule'
headers = {'Content-Type': 'application/json',
            'Authorization': 'JWT '}

#   get
def get():
    url_param = url + ''
    response = requests.get(url_param, headers=headers)
    print(response.text)
    assert response.status_code == 200

#   post
def post():
    data = {'start_time': '2020-11-11T11:11:11',
            'end_time': '2020-11-11T11:11:11',
            'description': 'thisisnew'}
    response = requests.post(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201

#   put
def put():
    data = {'personalSchedule_id': '1',
            'start_time': '2020-11-11T11:11:11',
            'end_time': '2020-12-10T10:10:10',
            'description': 'edited'}
    response = requests.put(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201

#   delete
def delete():
    url_param = url + '?personalSchedule_id=1'
    response = requests.delete(url_param, headers=headers)
    # print(response.text)
    assert response.status_code == 204


delete()