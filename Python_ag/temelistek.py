import requests

adres="http://www.google.com"
r=requests.get(adres)
print(r.history)