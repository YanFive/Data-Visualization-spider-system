"""1、微信公众号爬虫
2、图片表格文字识别"""
import re
import os
import requests
import codecs
import time
import pandas as pd
from aip import AipOcr
from lxml import etree
from bs4 import BeautifulSoup as bs

# 百度API Key
APP_ID = '18245800'
API_KEY = 'IgRj96QQ29ZEEzxR32TWvGpQ'
SECRET_KEY = 'ujh5O5KgidSEGwMpm8dUSTLuWF8m2EbG'

# 爬虫目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"  # 登录

# 使用cookie，跳过登录操作
headers = {
    "Cookie": "pgv_pvi=105238528; RK=2joVMokyW3; ptcz=941b0333c19c7ad4a57d50067c184c282ba3f1cad54e6cefe79b9554fa20a169; ua_id=DlSDKJMmPYteChcvAAAAAOeVGswsYSfaxdVeEaUnz-o=; noticeLoginFlag=1; remember_acct=1812094543%40qq.com; mm_lang=zh_CN; openid2ticket_ouxLV09zVogTLVxwjncUTk1GTLP4=LWhsEsBTVLfEX5gl3iqrl0fceP2Ir3g4rt5OJ8c1bjs=; pgv_si=s891224064; uuid=8614d8f738a13aa99e12949442b31a5c; rand_info=CAESIDUaNqpS9dmsmIyEgTtoE5v/CV6h7vobNsvN3MDRcdq1; slave_bizuin=3553956539; data_bizuin=3553956539; bizuin=3553956539; data_ticket=IqLonKmo33t3ftSCsL3xeyMHbaMBXcKXCl5AQq2AdY3gm0EYRKUyG3AnzEvg/5x5; slave_sid=eFJqa1Ridl9NSjNIQkMwUDJrN0hYUkx3VmV4OFpLSnFCVnV3Z3dZNUFaZUQyVVFLTEdnbW1QOEwzc2tMdjRWVnR4bUxRWm1zaFBiZEVLRDRLTGs1WEpYMFVrak1sWHNrSXp0dVNMS1o5anltYU9oUUE5eFFtWW1vN2xjd01OWHlBekFCcDRmVUxWb291SGZX; slave_user=gh_16f9ac91affd; xid=2774de77a7a067180c45a38f41ba2ca8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

data = {
    "token": "1254701162",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MzUwOTcwMjEyNA==",
    "type": "9",
}

def url_spider():
    content_list = []
    keyword = "最新估值统计"
    for i in range(11):
        data["begin"] = i * 5
        time.sleep(1)
        # get方法
        content_json = requests.get(url, headers=headers, params=data).json()
        # 返回json数据,包含每一页数据
        for item in content_json["app_msg_list"]:
            items = []
            if re.search(keyword, item["title"]):
                items.append(item["title"])
                items.append(item["link"])
                content_list.append(items)
        print(i)
    name = ['title', 'link']    # 设定CSV文件
    test = pd.DataFrame(columns=name, data=content_list)
    test.to_csv("url.csv", mode='a', encoding='utf-8-sig')
    print("保存成功")

def pic_spider():
    url_path = "F:/BKCX/Graduationdesign/Design/Design/url.csv"
    df = pd.read_csv(url_path)
    url_list = df["link"].tolist()  #文件中读取URL列表
    for url in url_list:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        soup = bs(response.content, features='lxml')
        html = etree.HTML(response.text)
        # 获取图片URL和名字
        img_name = html.xpath('//*[@id="activity-name"]/text()')[0].strip()[5:]
        img_s = soup.find('img', {'class': 'item item-image'})
        img_url = img_s['data-src']
        res = requests.get(url=img_url, headers=headers)
        local_path = "F:/BKCX/Graduationdesign/Design/Design/pic/"
        with codecs.open(local_path + '%s.jpg' % (img_name), 'wb') as f:
            f.write(res.content)

def get_pic(picpath): # 读图片
    with open(picpath, 'rb') as fp:
        return fp.read()

def xls_download(url, xlspath): # 写文件
    r = requests.get(url)
    with open(xlspath, 'wb') as f:
        f.write(r.content)

def orc():
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    pic_path = "F:/BKCX/Graduationdesign/Design/Design/pic"
    xls_path = "F:/BKCX/Graduationdesign/Design/Design/xls"
    for pic in os.listdir(pic_path):
        image = get_pic(os.path.join(pic_path, pic))
        url = client.tableRecognition(image)["result"]["result_data"]
        xls_name = pic.split('.')[0] + '.xls'
        xls_download(url, os.path.join(xls_path, xls_name))

if __name__ == "__main__":
    url_spider()
    pic_spider()
    orc()
