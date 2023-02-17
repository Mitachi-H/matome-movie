import cv2,json,os,glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class makeTile():
    def __init__(self,name,arranged = False,title = False):
        self.name = name
        self.title = title
        self.blank_tile = cv2.imread('./images/blank_tile.jpg') 
        self.font_path = "./07やさしさゴシック.ttf"
        self.wikiList = None
        self.tile_num = 1
        self.arranged = arranged

    def __call__(self):
        self.open_wikiList()
        files = glob.glob("./squares/"+self.name+"/*")
        for i,img_path in enumerate(files):
            #title によって場合分け
            tile = self.make_tile(img_path,self.title)
            try:
                text = self.wikiList[i-1]
            except IndexError:
                raise IndexError("textが不十分です")
            lineList = self.convert_to_lineList(text)

            y_start = 0 if self.title else 360
            final_tile = self.put_text(tile, lineList, y_start, fontFace=self.font_path, fontScale=25, color=(255,255,255))

            if final_tile is None:
                return
            self.save_tile(final_tile)


    def open_wikiList(self):
        if self.arranged:
            f = open("./arranged_wikiList/"+self.name+".json","r")
        else:
            f = open("./wikiList/"+self.name+".json","r")
        self.wikiList= json.load(f)
    
    def make_tile(self,img_path,title):
        img = cv2.imread(img_path)
        if img is None:
            return None
        if title:
            return None
        else:
            if not img.shape[0] == img.shape[1] == 360:
                raise ValueError("写真の大きさが不適切です")
            tile = self.blank_tile
            # 画像の合成
            tile[0:img.shape[0], 0:img.shape[1]] = img
        return tile

    # 参考記事　https://qiita.com/mo256man/items/82da5138eeacc420499d
    def put_text(self,tile, lineList, y_start, fontFace, fontScale, color):
        img_height,img_length,_ = tile.shape
        imgPIL = Image.fromarray(tile)
        draw = ImageDraw.Draw(imgPIL)

        line = len(lineList)
        # lineが多い時はmarginを小さく
        margin = 1.5 if line<=8 else 1.3
        # lineがかなり多い時はfontsizeを小さく
        if line >10:
            fontScale = 20
        fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
        
        for i,text in enumerate(lineList):
            w, h = draw.textsize(text, font = fontPIL)
            if i == 0:
                y_center = (y_start+img_height)/2
                textbox_height = h*margin*line
                line_start = y_center - textbox_height/2
            draw.text(xy = ((img_length-w)/2,line_start+h*margin*i), text = text, fill = color, font = fontPIL)
        return np.array(imgPIL, dtype = np.uint8)
    
    def convert_to_lineList(self,text,max_word_num = 13):
        line = len(text)//max_word_num
        # mecab を用いて、切り方の工夫しても良い
        lineList = [text[i*max_word_num:((i+1)*max_word_num if i!=line else len(text))] for i in range(0,line+1)]
        return lineList

    def save_tile(self,tile):
        dirpath = "./tiles/"+self.name
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        tile_path = dirpath + "/" + self.name +str(self.tile_num) + ".jpg"
        cv2.imwrite(tile_path,tile)
        self.tile_num+=1