import requests,re,json
from bs4 import BeautifulSoup

persons =[]
url = "https://ja.wikipedia.org/wiki/2022_FIFA%E3%83%AF%E3%83%BC%E3%83%AB%E3%83%89%E3%82%AB%E3%83%83%E3%83%97%E6%97%A5%E6%9C%AC%E4%BB%A3%E8%A1%A8#%E7%99%BB%E9%8C%B2%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC"
r = requests.get(url)
# HTTPerror 処理
r.raise_for_status()
soup = BeautifulSoup(r.text,"html.parser")
table =  soup.select("table.wikitable")[0]
for tr in table.select("tbody > tr"):
    td = tr.select("td")
    if len(td)>0:
        persons.append(td[0].get_text().strip())
print(persons)