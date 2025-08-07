import requests
import base64
url="1.1.1.1"
f = open("user.txt","r")
for i in f:
    print(i.strip())
    encoded=base64.b64encode(i.encode())
    print(encoded.decode())
    response=requests.get(url,headers=headers)
    headers={'Authorization':'Basic'+encoded}
    print(response.text)
    if int(response.status_code==401):
        print(i.strip())