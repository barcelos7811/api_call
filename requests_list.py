import os, sys
import json, requests

os.environ['NO_PROXY'] = '127.0.0.1'
# deu certo
# r = requests.get('http://127.0.0.1:5000/list_all_call')
# texto = 'atendimento'
# texto = 12
# print(texto)
id = 12
id_string = str(id)
print(id_string)
print(id)
my_json = {'login': 'ADM', 'password': '123'}
dd = "http://127.0.0.1:5000/find_call_id/"
print(dd)
url = dd
# url = 'http://127.0.0.1:5000/find/12'
# r = requests.post('http://127.0.0.1:5000/find_call_id/12/') deu certo
r = requests.get(url, json=my_json).json()
print(r.get("id"))
y = json.dumps(r)
print(y)
print(json.dumps(["apple", "bananas"]))

print(r)
print(r.json())
print(r.content)

print(sys.stdout.encoding)


# r = requests.post('http://127.0.0.1:5000/find_call/'+texto+'/')
# r = requests.post('http://127.0.0.1:5000/find_call_id/{{texto}}/')
# r = requests.post('http://127.0.0.1:5000/find_call_id/id/')
# req = requests.post('https://mywebsite.com/pageB', data={'fieldB': 'value_you_want_to_submit'})
# r = requests.post('/xyz/api/pqr/', params=Params)
