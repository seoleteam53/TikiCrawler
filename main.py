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
        time.sleep(2)
    def request_html(self,url):
        self.driver.get(url)
        self.driver.set_page_load_timeout(100)
        self.scroll()

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
    def get_comments(self,url,filesave_name):
        self.request_html(url)
        self.driver.implicitly_wait(7)
        linkNX = self.driver.find_elements_by_class_name("-reviews-count")
        if linkNX != [] :
            try:
                totalNX = int(linkNX[0].text)
            except:
                print("an error has been raised")
                return 0
            linkNX[0].click()
            time.sleep(3)
            NX_Tag = self.driver.find_elements_by_class_name("review_detail")
            comments = []
            if NX_Tag != [] :
                for tag in NX_Tag :
                    if tag.find_elements_by_tag_name('span') != []:
                        comments.append(tag.find_elements_by_tag_name("span")[0].text)
                print(comments)
                if comments != [] :
                    self.save_data(filesave_name,comments)
                    return 1
                else :
                    return 0
            else:
                return 0
            time.sleep(30)
        else :
            return 0
    def save_data(self,filename,data):
        with open(filename,"a",encoding = 'utf-8') as fw:
            for x in data :
                fw.write(b'"'.decode('utf-8') + x + b'",'.decode('utf-8') + "\n")
        fw.close()
    def auto_get_comments(self, link_sub_catagory):
        self.request_html(link_sub_catagory)
        self.driver.implicitly_wait(7)
        sub_catagory_tag = self.driver.find_elements_by_class_name("filter-list-box")
        file_name = ""
        if sub_catagory_tag != []:
            file_name = "data\\" + ''.join(re.findall('(\w+)',sub_catagory_tag[0].find_elements_by_tag_name('h1')[0].text)) + ".crash"
        else :
            return 0
        print(file_name)
        product_tag = self.driver.find_elements_by_class_name("product-item")
        product_list_tag = []
        if product_tag != []:
            product_list_tag = product_tag[:47]
        else :
            return 0
        link_products = [x.find_elements_by_tag_name('a')[0].get_attribute('href') for x in product_list_tag]
        if link_products != []:
            for link in link_products:
                if link != None :
                    i = self.get_comments(link,file_name)
                    if i == 0 :
                        continue
                    time.sleep(5)
            return 1
        else :
            return 0

    def close_driver(self):
        print("program wil be turn off in 5 seconds")
        time.sleep(5)
        self.driver.quit()

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
    #tiki.get_comments("https://tiki.vn/may-tinh-bang-masstel-tab-10-plus-hang-chinh-hang-p11627000.html?src=category-page-1789.1794&2hi=0","here.crash")
    sub_catagories_link = read("sub_catagories.json")
    
    collected_link = []
    try :
        collected_link = read("collected_link.crash")
    except:
        print("there is no link in that file! ")
    print(collected_link)
    for sub_catagory in sub_catagories_link:
        if sub_catagory != [] :
            for sub_link in sub_catagory:
                if sub_link != [] and sub_link not in collected_link :
                    i = tiki.auto_get_comments(sub_link)
                    collected_link.append(sub_link)
                    save("collected_link.crash",collected_link)
    tiki.close_driver()
if __name__ == '__main__' :
    main()
