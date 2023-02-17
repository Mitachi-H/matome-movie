import json
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

class arrangeText():
    def __init__(self,name,mode="auto"):
        self.name = name
        self.wikis = ""
        self.mode = mode
        self.arrange ={"manual":self.manual_arrange,"auto":self.auto_arrange}
        self.arranged_wikiList = []
        self.image_num = 0
    
    def __call__(self):
        self.open_wikis()
        self.arrange[self.mode]()
        self.update_json()
        return self.image_num

    def open_wikis(self):
        f = open("./wikis/"+self.name+".txt","r+")
        self.wikis= f.read()
    
    def auto_arrange(self):
        if self.wikis.count("。")<10:
            raise ValueError
        # 自動要約のオブジェクトを生成
        auto_abstractor = AutoAbstractor()
        # トークナイザー（単語分割）にMeCabを指定
        auto_abstractor.tokenizable_doc = MeCabTokenizer()
        # 文書の区切り文字を指定
        auto_abstractor.delimiter_list = ["。"]
        # キュメントの抽象化、フィルタリングを行うオブジェクトを生成
        abstractable_doc = TopNRankAbstractor()
        # 文書の要約を実行
        result_dict = auto_abstractor.summarize(self.wikis, abstractable_doc)
        for text in result_dict["summarize_result"]:
            self.arranged_wikiList.append(text)
            self.image_num+=1
    
    def update_json(self):
        f = open("./arranged_wikiList/"+self.name+".json","w")
        json.dump(self.arranged_wikiList,f,ensure_ascii=False)

    def manual_arrange(self):
        pass
        # for i,dict_ in enumerate(self.jsons):
            # text = self.input_word(dict_,"text")
            # # wikiのエピソードを使うかどうかで場合分け
            # if not text:
            #     continue
            # arrange_json={}
            # arrange_json["text"] = text
            # arrange_json["title"] = self.input_word(dict_,"title")
            # self.arranged_wikiList.append(arrange_json)
    
    # def input_word(self,dict_,word):
    #     # word is text or title
    #     option = "（変更がない場合はEnterを入力、無視の場合は n と入力）"
    #     while True:
    #         if word == "text":
    #             print("\n---wiki---\n")
    #             print(dict_["wiki"])
    #             print("\n---wiki---\n")
    #         # text 入力の場合のみ option 表示
    #         str_ = input(word+"を入力してください"+(option if word == "text" else "")+"\n")
    #         if str_ == "n":
    #             return None
    #         if not str_:
    #             if word =="text":
    #                 str_ = dict_["wiki"]
    #             else:
    #                 continue
    #         print("\n\n\n")
    #         print("\n---"+word+"---\n")
    #         print(str_)
    #         print("\n---"+word+"---\n")
    #         if input("こちらでよろしいですか？{y/n}")=="y":
    #             return str_