# from django.test import TestCase
import requests

# Create your tests here.
url = 'http://localhost:8000/api/'
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
    data = {'group_id': '1',
            'description': 'letgo'}
    response = requests.post(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201

#   put
def put():
    data = {'groupNotice_id': '5',
            'description': 'edited test'}
    response = requests.put(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201

#   delete
def delete():
    url_param = url + '?groupNotice_id=5'
    response = requests.delete(url_param, headers=headers)
    # print(response.text)
    assert response.status_code == 204


get()