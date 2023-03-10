from retinaface import RetinaFace
import cv2,os,glob
import matplotlib.pyplot as plt

class cutImage():
    def __init__(self,name):
        self.name = name
        self.square_num = 1

    def __call__(self):
        """
        画像をファイルを読み込み、適切なものを選択する
        その後正方形に変換して保存する
        """
        files = glob.glob("./images/"+self.name+"/*")
        for img_path in files:
            cut_img = self.arrange_to_square(img_path)
            if not cut_img is None:
                self.save_square(cut_img)
    
    # 参考記事 https://self-development.info/%E3%80%90python%E3%80%91retinaface%EF%BC%88retina-face%EF%BC%89%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/#:~:text=%E3%81%A6%E3%81%84%E3%81%8D%E3%81%BE%E3%81%99%E3%80%82-,RetinaFace%EF%BC%88retina%2Dface%EF%BC%89%E3%81%A8%E3%81%AF%EF%BC%9F,%E8%AA%8D%E8%AD%98%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA%E3%81%A8%E3%81%84%E3%81%86%E3%81%93%E3%81%A8%E3%81%A7%E3%81%99%E3%80%82
    def arrange_to_square(self,img_path):
        """
        顔を左右の中心にして360*360に切り出す
        顔が複数検知された場合はその写真を無視する
        """
        img= cv2.imread(img_path)
        resp = RetinaFace.detect_faces(img_path, threshold = 0.95)

        # 顔が複数なら
        if len(resp) !=1:
            return None
        
        # 顔が「左右」の中心にくるように画像を切り取る
        facial_area = resp["face_1"]["facial_area"]
        face_xcenter = (facial_area[0]+facial_area[2])/2
        face_ycenter = (facial_area[1]+facial_area[3])/2

        img_height,img_length,_ = img.shape

        xcenter_to_side = min(face_xcenter,img_length - face_xcenter)

        # 顔が左右の中心になるように画像を切り取ったとき、その画像が縦長か、横長か判定する
        portrait = img_height > xcenter_to_side*2

        # 縦長なら
        if portrait:
            # 横幅を正方形の長さとして、画像を切り出す
            face_in_upper_side = face_ycenter < img_height/2
            starty = 0 if face_in_upper_side else img_height - 2*xcenter_to_side
            endy = 2*xcenter_to_side if face_in_upper_side else img_height
            cut_img = img[int(starty):int(endy),int(face_xcenter-xcenter_to_side) : int(face_xcenter+xcenter_to_side)]
            pass
        else:
            # 縦幅を正方形の長さとして、画像を切り出す
            cut_img = img[:,int(face_xcenter-img_height/2) : int(face_xcenter+img_height/2)]
        
        # 画像サイズを360*360に変えて出力する
        return cv2.resize(cut_img,(360,360))
    
    def save_square(self,tile):
        """
        得られた正方形の写真を保存する
        """
        dirpath = "./squares/"+self.name
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        tile_path = dirpath + "/" + self.name +str(self.square_num) + ".jpg"
        cv2.imwrite(tile_path,tile)
        self.square_num+=1
