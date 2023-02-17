import requests,re,json
from bs4 import BeautifulSoup

persons =[]
url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E3%82%B5%E3%83%83%E3%82%AB%E3%83%BC%E9%81%B8%E6%89%8B%E4%B8%80%E8%A6%A7"
r = requests.get(url)
# HTTPerror 処理
r.raise_for_status()
soup = BeautifulSoup(r.text,"html.parser")
for ul in soup.select("div.div-col > ul"):
    for li in ul.select("li"):
        persons.append(li.get_text())
