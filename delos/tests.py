# from django.test import TestCase
import requests

# Create your tests here.

url = 'http://localhost:8000/api/survey'

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
    data = {'title': 'qtitle',
            'description': 'qdescription',
            'target_gender': 'M',
            'target_age_start': 2,
            'target_age_end': 5,
            'question' : [
                {'index': 1, 'content': '이것은 객관식질문1', 'type': 1, 'choices': '1.사과;2.배;3.감'},
                {'index': 2, 'content': '이것은 주관식질문', 'type': 2, 'choices': ''},
                {'index': 3, 'content': '이것은 객관식질문2', 'type': 1, 'choices': '1.사과2;2.배2;3.감2'}
            ]
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    assert response.status_code == 201


#   put
def put():
    data = {'survey_id': 7}
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
