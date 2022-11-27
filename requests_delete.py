import json, requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'
url = 'http://127.0.0.1:5000/delete_call_/2'
# myobj = {'title': 'dipirona cinco alterado', 'content': 'dipirona sódica cinco alterado'}

r = requests.delete(url)

print(r)
print(r.content)
# print(r.json())