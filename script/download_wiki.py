import requests,re,json
from bs4 import BeautifulSoup

class downloadWiki():
    def __init__(self,name):
        self.name = name
        self.url = "https://ja.wikipedia.org/wiki/"+name
        self.soup = None
        self.wiki = ""
        self.wikiList = []
        self.hashtagList = []
        self.image_num = 0
    
    def __call__(self,least_num=8):
        self.get_soup()
        self.main()
        if self.image_num >= least_num:
            self.save_wiki_and_hashtag()
        return self.image_num

    def get_soup(self):
        r = requests.get(self.url)
        # HTTPerror 処理
        r.raise_for_status()
        self.soup = BeautifulSoup(r.text,"html.parser")

    def main(self):
        # タグ抽出
        for li in self.soup.select("div.mw-normal-catlinks > ul > li"):
            self.update_hashtag(li.get_text())
        # 動画文章抽出
        for subNode in self.soup.select("a.vector-toc-link"):
            subtitle = subNode.get_text().strip()
            check = False
            keywords = ["エピソード","プレースタイル","人物","評価"]
            for keyword in keywords:
                if keyword in subtitle:
                    check=True
            if check:
                id = subNode.get("href")
                h2_3 = self.soup.select_one(id).parent
                # ダサ処理
                ul = h2_3.next_sibling.next_sibling
                #ul-li形式で書かれている場合
                if str(ul).startswith("<ul>"):
                    self.getEpisode_from_ul(ul)
                #pの羅列で書いている場合
                else:
                    self.getEpisode_from_p(ul)
    
    def getEpisode_from_ul(self,ul):
        for li in ul.children:
            text = li.get_text()
            self.update_wiki(text)

    def getEpisode_from_p(self,ul):
        tag=ul.next_sibling
        #hタグまでのp要素を取得
        while not str(tag).startswith("<h"):
            if str(tag).startswith("<p>"):
                text = tag.get_text()
                self.update_wiki(text)
            tag = tag.next_sibling
    
    def update_wiki(self,text):
        # 引用マーク削除
        text = re.sub(r"\[\d*?\]","",text)
        #　改行削除
        text = re.sub("\n","",text)
        # 空じゃないなら
        if text:
            self.wiki+=text
            # textが長すぎる場合前半後半に分割する
            if len(text) > 13*10: # 一行13文字　＊　10列
                for text_ in self.split_text(text):
                    self.wikiList.append(text_)
                    self.image_num+=1
            else:
                self.wikiList.append(text)
                self.image_num+=1
    
    def update_hashtag(self,text):
        if text.startswith("日本の"):
            text = text.replace("日本の","")
        if text.endswith("の人物"):
            text = text.replace("の人物","")
        self.hashtagList.append(text)
        pass

    def split_text(self,text):
        chunk = ""
        # かぎかっこ内のフラッグ
        flag = False
        textList = []
        for word in text:
            if word == "。":
                if not flag:
                    textList.append(chunk)
                    chunk = ""
                else:
                    chunk+=word
            else:
                if word == "「":
                    flag = True
                if word == "」":
                    flag = False
                chunk+=word
        return textList
        
    def save_wiki_and_hashtag(self):
        with open("./wikis/"+self.name+".txt","w") as f:
            f.write(self.wiki)

        with open("./wikiList/"+self.name+".json","w") as f:
            json.dump(self.wikiList,f,ensure_ascii=False)

        with open("./hashtagList/"+self.name+".json","w") as f:
            json.dump(self.hashtagList,f,ensure_ascii=False)
        
    