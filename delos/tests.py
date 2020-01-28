# from django.test import TestCase
import requests

# Create your tests here.
url = 'http://localhost:8000/api/timeTable'
headers = {'Content-Type': 'application/json',
            'Authorization': 'JWT '}


#   get
def get():
    url_param = url + '?group_id=1'
    response = requests.get(url_param, headers=headers)
    print(response.text)
    assert response.status_code == 200


#   post
def post():
    data = {'title': '시간표',
            'location': '장소',
            'day': '월화',
            'start_time': '22:08:47',
            'end_time': '22:08:47'
            }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    assert response.status_code == 201


#   put
def put():
    data = {'timeTable_id': '7',
            'title': '시간표11',
            'location': '장소11',
            'day': '화수',
            'start_time': '22:08:48',
            'end_time': '22:08:49'
            }
    response = requests.put(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201


#   delete
def delete():
    url_param = url + '?timeTable_id=6'
    response = requests.delete(url_param, headers=headers)
    # print(response.text)
    assert response.status_code == 204


delete()