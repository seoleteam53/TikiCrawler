import sys
import os
import selenium
import pyautogui
import options
from selenium import webdriver
from options import Options,attrs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import re

path_root = "https://tiki.vn"
file_Catagories = "catagories.json"
name_class_sub_catagories = "list-group-item is-child"
file_sub_Catagories = "sub_catagories.json"
class Tiki :
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(executable_path = "./chromedriver.exe",options = options)
        self.driver.maximize_window()
    def scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while (True) :
            self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height :
                break
            else :
                last_height = new_height      
        time.sleep(3)
    def request_html(self,url):
        self.driver.get(url)
        self.driver.set_page_load_timeout(100)
        #self.scroll()

    def get_catagory(self,root):
        self.request_html(root)
        aTag = self.driver.find_elements_by_class_name("MenuItem__MenuLink-tii3xq-1")
        catagories = []
        if aTag != []:
            for a in aTag :
                catagories.append(a.get_attribute('href'))
        return catagories
    def get_sub_catagory(self,catagory):
        self.request_html(catagory)
        sub_link = []
        sub_catagories_Tag = self.driver.find_elements_by_class_name("is-child")
        if sub_catagories_Tag != []:
            for subTag in sub_catagories_Tag :
                if subTag.find_elements_by_tag_name('a') != []:
                    sub_link.append(subTag.find_elements_by_tag_name('a')[0].get_attribute('href'))
        return sub_link
    def get_comments(self,url):
        self.request_html(url)
        linkNX = self.driver.find_elements_by_class_name("-reviews-count")
        if linkNX != [] :
            totalNX = int(linkNX[0].text)
            linkNX[0].click()
            time.sleep(3)
            NX_Tag = self.driver.find_elements_by_class_name("review_detail")
            if NX_Tag != [] :
                for tag in NX_tag :
                    if tag.find_elements_by_tag_name('span') != []:
                        print(tag.find_elements_by_tag_name('span')[0].text)

            else :
                print("no name")
            time.sleep(30)
        else :
            return 0
def save(file_name,Llink):
    tmp = json.dumps(Llink,indent = 4)
    with open(file_name, 'w',encoding = 'utf-8') as fw:
        fw.write(tmp)
    fw.close()

def read(file_name):
    data = {}
    with open(file_name,'r',encoding = 'utf-8') as fr:
        data = json.load(fr)
    fr.close()
    return data
     
def main():
    tiki = Tiki()
    tiki.get_comments("https://tiki.vn/dien-thoai-samsung-galaxy-a10s-32gb-2gb-hang-chinh-hang-p25918805.html?src=category-page-1789.1795&2hi=0")
    

if __name__ == '__main__' :
    main()
