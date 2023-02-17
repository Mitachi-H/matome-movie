import shutil,os,cv2
import numpy as np

from requests.exceptions import HTTPError
from script.download_wiki import downloadWiki
from script.make_description import makeDescription
from script.arrange_text import arrangeText
from script.download_image import downloadImage
from script.cut_image import cutImage
from script.make_tile import makeTile
from script.make_video import makeVideo

def delete_files(dir_names):
    """
    指定したdir内のファイルを削除する関数
    imageにはblank画像が必要なので削除した場合は追加する
    """
    for target_dir in dir_names.keys():
        if dir_names[target_dir]:
            shutil.rmtree(target_dir)
            os.mkdir(target_dir) 
            if target_dir=="images":
                #ブランク画像
                height = 720
                width_tile = 360
                width_movie = 1280
                blank_tile = np.zeros((height, width_tile, 3))
                blank_movie = np.zeros((height, width_movie, 3))
                cv2.imwrite('./images/blank_tile.jpg',blank_tile)
                cv2.imwrite('./images/blank_movie.jpg',blank_movie)

# delete_files({
#         "arranged_wikiList":True,
#         "description":True,
#         "hashtagList":True,
#         "images":True,
#         "movies":True,
#         "squares":True,
#         "tiles":True,
#         "wikiList":True,
#         "wikis":True,
# })

def main(persons,arranged = False,least_num=8):
    """
    各ファイルのclassを呼び出し実行する。
    """
    for person in persons:
        try:
            image_num = downloadWiki(person)(least_num)
            makeDescription(person)()
            if arranged:
                image_num = arrangeText(person)()

        except (ValueError,HTTPError) as E:
            print(E)
            print(f"人物：{person}--Wikipediaにアクセスできないか、または情報が不十分です--")
            continue

        try:
            downloadImage(person)(image_num)
            cutImage(person)()
            makeTile(person)()
        except (FileNotFoundError,IndexError) as E:
            print(E)
            print(f"人物：{person}--textが十分でない可能性があります--")
        makeVideo(person)()

persons = []
main(persons)
