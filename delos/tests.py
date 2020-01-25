# from django.test import TestCase
import requests

# Create your tests here.
url = 'http://localhost:8000/api/groupBoard'
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
            'description': '할일',
            'due_date': '2020-11-11T11:11:11',
            'person_in_charge': [1, 2]
            }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    assert response.status_code == 201

#   put
def put():
    data = {'groupBoard_id': '6',
            'description': 'String',
            'due_date': '2020-11-11T12:12:12',
            'person_in_charge': [2]
            }
    response = requests.put(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201

#   delete
def delete():
    url_param = url + '?groupBoard_id=6'
    response = requests.delete(url_param, headers=headers)
    # print(response.text)
    assert response.status_code == 204


delete()