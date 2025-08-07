import requests
from bs4 import BeautifulSoup

url="https://www.exploit-db.com"
istek=requests.get(url)
parser=BeautifulSoup(istek.text,'html.parser')
hrefs=parser.find_all("href")
print(hrefs)