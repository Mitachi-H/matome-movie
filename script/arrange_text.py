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
    
    def __call__(self)->int:
        """
        Wikipediaで収集した情報を要約して、小さな塊に分けて保存数
        その数に合わせて、必要になる写真の枚数を返す
        """
        self.open_wikis()
        self.arrange[self.mode]()
        self.update_json()
        return self.image_num

    def open_wikis(self):
        """
        Wikipediaで収集した情報が保存されたファイルを開き、その内容をwikisに保存する
        """
        f = open("./wikis/"+self.name+".txt","r+")
        self.wikis= f.read()
    
    # 参考記事　https://resanaplaza.com/2022/05/19/%E3%80%90%E5%AE%9F%E8%B7%B5%E3%80%91python%EF%BC%8Bpysummarization%E3%81%A7%E6%96%87%E6%9B%B8%E8%A6%81%E7%B4%84%EF%BC%88%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%83%9E%E3%82%A4%E3%83%8B%E3%83%B3/
    def auto_arrange(self):
        """
        pysummarizationを用いて要約 arraged_wikiListに保存
        """
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
        """
        要約して得た arranged_wikiListをファイルに保存する
        """
        f = open("./arranged_wikiList/"+self.name+".json","w")
        json.dump(self.arranged_wikiList,f,ensure_ascii=False)

    def manual_arrange(self):
        """
        お試しで追加した機能、完全自動化したかったので却下
        """
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