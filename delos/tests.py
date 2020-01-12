# from django.test import TestCase
import requests, json

# Create your tests here.

URL = 'http://114.108.49.11:9157/api/createGroup/'
headers = {'Content-Type': 'application/json; charset=utf-8'}
data = {
    "name": "good", 
    "description": "pythonpostrequestgroup"
    }

res = requests.post(URL, data=json.dumps(data), headers=headers)

print(res)