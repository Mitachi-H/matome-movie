import cv2,glob
import numpy as np
import matplotlib.pyplot as plt
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont

class makeVideo():
    def __init__(self,name,fps = 30,required_time = 15):
        self.name = name
        self.tiles = []
        self.video = None
        self.font_path = "./07やさしさゴシック.ttf"

        self.fps = fps
        self.required_time = required_time

        self.blank_movie = cv2.imread("./images/blank_movie.jpg")
        self.blank_tile = cv2.imread("./images/blank_tile.jpg")
        self.title_tile = None
    
    def __call__(self):
        self.open_tiles()
        self.add_title_tile()
        self.set_video()
        self.add_frame()
        self.video.release()
        self.add_song()
    
    def open_tiles(self):
        files = glob.glob("./tiles/"+self.name+"/*")
        for tile_path in files:
            self.tiles.append(cv2.imread(tile_path))
        self.tiles.append(self.blank_tile)
    
    def set_video(self):
        self.video = cv2.VideoWriter('./movies/'+self.name+'.mp4',
                      cv2.VideoWriter_fourcc(*"mp4v"),
                      self.fps, (1280, 720))
    
        # 参考記事　https://qiita.com/mo256man/items/82da5138eeacc420499d
    def add_title_tile(self):
        fontFace = self.font_path
        fontScale = 100
        color=(255,255,255)

        title = self.name+" エピソード"

        camera_height,camera_length,_ = self.blank_movie.shape
        imgPIL = Image.fromarray(self.blank_movie)
        draw = ImageDraw.Draw(imgPIL)
        fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
        
        w, h = draw.textsize(title, font = fontPIL)
        draw.text(xy = ((camera_length-w)/2,(camera_height-h)/2), text = title, fill = color, font = fontPIL)
        self.title_tile = np.array(imgPIL, dtype = np.uint8)
    
    def add_frame(self):
        # 最初の数秒はtitleを見せる
        first_second = 2
        for _ in range(first_second*self.fps):
            self.video.write(self.title_tile)
        
        start_line = 1280
        tile_length = 360
        camera_length = 1280
        # それぞれのtileの右端の位置
        tiles_pos = [start_line + tile_length * i for i in range(len(self.tiles))]
        # blankでないtileの右端を得る
        last_tile_left = tiles_pos[-1]
        # カメラが1frameごとに進むスピード
        camera_speed = int(camera_length/(self.fps*self.required_time))
        # カメラの左端の位置
        camera_left = 0

        # そのあと動き出す
        while camera_left <= last_tile_left:
            frame = self.blank_movie
            # titleについて
            if camera_left <= camera_length:
                frame[0:self.title_tile.shape[0],0:camera_length - camera_left] = self.title_tile[:,camera_left:camera_length]
            # tileについて
            for tile,tile_pos in zip(self.tiles,tiles_pos):
                # カメラの画角にtileがある場合は
                if camera_left <= tile_pos + tile_length and tile_pos <= camera_left + camera_length :
                    # 画面上のtileの位置
                    left_pos = tile_pos-camera_left
                    right_pos = left_pos + tile_length
                    # tileの表示範囲
                    tile_start = 0
                    tile_end = tile_length
                    # tileが見切れている場合
                    if left_pos <= 0:
                        tile_start = - left_pos
                        left_pos = 0
                    if right_pos >= camera_length:
                        tile_end = camera_length - left_pos
                        right_pos = camera_length
                    # tileを画面の指定位置に描画
                    frame[0:tile.shape[0],left_pos:right_pos] = tile[:,tile_start:tile_end]
            self.video.write(frame)
            camera_left += camera_speed

    def add_song(self,bgm_num=1):      
        video_path ='./movies/'+self.name+'.mp4'      
        chumk_path = "./movies/aaa.mp4" 

        clip = mp.VideoFileClip(video_path).subclip()
        clip.write_videofile(chumk_path)        
        # mp4 H.264に変換                                             
        new_clip = mp.VideoFileClip(chumk_path).subclip()
        duration = new_clip.duration
        last_second = 10
        audio_clip = mp.AudioFileClip("./songs/bgm1.mp3").subclip(0,duration+last_second)
        new_clip.set_audio(audio_clip).write_videofile(video_path)