import json

class makeDescription():
    def __init__(self,name):
        self.name = name
        self.hashtagList = []
        self.description = {}

    def __call__(self):
        self.get_hashtagList()

        if len(self.hashtagList)==0:
            return
        
        firsttag = self.hashtagList[0]
        if firsttag==self.name:
            firsttag=self.hashtagList[1]
        title = "【"+firsttag+"】 "+self.name+"エピソードまとめ"
        description = self.name+"""のエピソードを wikipedia の情報をもとにまとめてます。
この動画は自動で作成されたものです。

"""
        for hashtag in self.hashtagList:
            description+="#"+hashtag+" "
        
        self.description["tilte"]=title
        self.description["description"]=description

        self.save_description()
        pass
    
    def get_hashtagList(self):
        with open("./hashtagList/"+self.name+".json","r") as f:
            self.hashtagList= json.load(f)
    
    def save_description(self):
        with open("./description/"+self.name+".json","w") as f:
            json.dump(self.description,f,ensure_ascii=False)
