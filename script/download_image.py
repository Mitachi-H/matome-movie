import urllib.request
import os
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

class downloadImage():
    def __init__(self,name):
        self.name = name
        self.i = 1
        self.options = ChromeOptions()
    
    def __call__(self,image_num):
        """
        指定された枚数+予備の枚数をgoogle写真検索からdownloadする
        """
        spare = 10
        self.download_image(image_num + spare)
    
    def download_image(self,image_num=20,keyword=""):
        """
        google画像検索から写真を保存する
        keyword が指定されている場合はそれも含めて検索する
        必要な画像数が多い場合は、適宜スクロールを行いHTMLを更新する
        """
        self.options.headless = True
        driver = Chrome(options=self.options)
        driver.get("https://www.google.com/imghp?hl=ja_JP")
        driver.maximize_window()

        input_element = driver.find_element_by_name("q")
        input_element.send_keys(self.name+" "+keyword if keyword else self.name)
        input_element.send_keys(Keys.RETURN)

        assert "Google" in driver.title

    #参考記事　https://qiita.com/Cartelet/items/2f54965850c201f4fb96
        if image_num > 30:
            for t in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1.5)
            try:driver.find_element_by_class_name("mye4qd").click() #「検索結果をもっと表示」ってボタンを押してる
            except:pass
            if image_num > 150:
                for t in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.5)

        # driver.save_screenshot("search_results.png")

        dirpath = "./images/"+self.name
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        for imgNode in driver.find_elements_by_css_selector("div.bRMDJf > img"):
            if self.i > image_num:
                driver.quit()
                return
            url = imgNode.get_attribute("src")
            if url:
                r = urllib.request.urlopen(url)
                # 画像ファイル種類を判別して保存できればいいなぁ
                with open (dirpath+"/"+self.name+str(self.i)+".jpg","wb") as f:
                    f.write(r.read())
                self.i+=1