import json, requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'
# 01 - PESQUISAR O ITEM QUE DSEJA ALTERAR
id = 16
id_string = str(id)
url1 = 'http://127.0.0.1:5000/find_call_id/'+(id_string)
result = requests.post(url1).json()
print('result:')
print(result)
# 02 - ALTERAR O ITEM QUE FOI SELECIONADO
url = 'http://127.0.0.1:5000/update_call_/'+(id_string)
my_json = {'id': id, 'id_status': 1, 'description': 'teste ricardo', 'id_kind': 1, 'id_user': 1}
print('my_json:')
print(my_json)
data = my_json
r = requests.put(url, json=data)
print(r)
print(r.content)