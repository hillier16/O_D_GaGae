# from django.test import TestCase
import requests

# Create your tests here.


url = 'http://localhost:8000/api/surveyAnswer'
headers = {'Content-Type': 'application/json',
            'Authorization': 'JWT '}

#   get
def get():
    url_param = url + '?survey_id=1'
    response = requests.get(url_param, headers=headers)
    print(response.text)
    assert response.status_code == 200


#   post
def post():
    data = {'survey_question_id': '1',
            'content': '대답'}
    response = requests.post(url, json=data, headers=headers)
    # print(response.text)
    assert response.status_code == 201


#   put
def put():
    data = {'survey_id': '1'}
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
