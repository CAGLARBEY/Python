import requests
from bs4 import BeautifulSoup
url1="https://x.com/haluktatar/status/1847655219796332916"
response=requests.get(url1)
parser=BeautifulSoup(response.text, 'html.parser')
spans=parser.find_all("span",{"class0":"s-post"})
for s in spans:
    print(s)