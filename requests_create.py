import json, requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'
url = 'http://127.0.0.1:5000/create_call_'
myobj = {'id_user': 1, 'id_kind': 1, 'id_status': 1, 'description': 'TESTE 002 54 32'}


r = requests.post(url, json=myobj)

print(r)
print(r.content)