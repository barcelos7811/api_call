import os, sys
import json, requests

os.environ['NO_PROXY'] = '127.0.0.1'
usr = "ADM"
pas = "123"
# id_string = str(id)
# print(id_string)
url = "http://127.0.0.1:5000/find_user_login_/"+usr+"/"+pas+"/"
r = requests.get(url)
print(r)
print(r.json())
if r == []:
    print('não existe dados')
else:
    print('existe dados')
