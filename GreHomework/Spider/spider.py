# -*- coding = utf-8 -*-
# @Time : 2022/6/20 23:51
# @Author : bai_zhou
# @File : spider.py
# @Software : PyCharm

import sqlite3
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt


def main():
    print("Start...")
    dbpath = '../books.db'
    baseurl = 'https://book.douban.com/top250?start='
    datalist = getDate(baseurl)
    saveDataDB(datalist, dbpath)


#正则表达式
findLink = re.compile(r'<a href="(.*?)".*?>')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<a .* title="(.*?)">')
findTitle_f = re.compile(r'(?!<br/>)\s*<span style="font-size:12px;">(.*?)</span>')
findTitle_s = re.compile(r'<br/>\s*<span style="font-size:12px;">(.*?)</span>')
findRating = re.compile(r'<span class="rating_nums">(.*)</span>')
findJurdge = re.compile(r'<span class="pl">\(\s*(\d*)人评价\s*\)</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findOther = re.compile(r'<p class="pl">(.*?)</p>', re.S)

def getDate(baseual):
    datalist = []

    for i in range(10):
        url = baseual + str(i * 25)
        html = askURL(url)
        print("开始解析第{}页...".format(i+1))
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('tr', class_='item'):
            data = []
            item = str(item)

            #print(item)
            s_link = re.findall(findLink, item)[0]
            data.append(s_link)

            s_imgSrc = re.findall(findImgSrc, item)[0]
            data.append(s_imgSrc)

            s_title = re.findall(findTitle, item)[0]
            s_titlef = re.findall(findTitle_f, item)
            if len(s_titlef) >= 1:
                s_title = s_title + s_titlef[0]
            data.append(s_title)

            s_titles = re.findall(findTitle_s, item)
            if len(s_titles) >= 1:
                data.append(s_titles[0])
            else:
                data.append(" ")

            s_score = re.findall(findRating, item)[0]
            data.append(s_score)

            s_num = re.findall(findJurdge, item)[0]
            data.append(s_num)

            s_inq = re.findall(findInq, item)
            if len(s_inq) >= 1:
                data.append(s_inq[0])
            else:
                data.append(' ')

            s_other = re.findall(findOther, item)[0]
            s_other = s_other.split('/')
            if len(s_other) >= 1:
                author = s_other[0].replace(' ','')
                for i in range(1, len(s_other)-3):
                    author = author + '/' + s_other[i].replace(' ','')
                data.append(author)
                data.append(author)
                cbs = s_other[-3].replace(' ','')
                data.append(cbs)
                ti = s_other[-2].replace(' ','')
                data.append(ti)
                price = s_other[-1].replace(' ','')
                price = price.replace('元','') + '元'
                data.append(price)
            else:
                data.append(' ',' ',' ',' ')
            datalist.append(data)
            print(data)
    return datalist


def saveDataDB(datalist, DBpath):
    print("正在保存数据...")
    init_db(DBpath)
    conn = sqlite3.connect(DBpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into Book250
            (
            info_link,pic_link,cname,fname,score,rated,instruction,authors,writer,publisher,time,price
            )
            values(%s)
        '''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(DBpath):
    sql = '''
        create table Book250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname text,
        fname text,
        score numeric,
        rated numeric,
        instruction text,
        authors text,
        writer text,
        publisher text,
        time text,
        price text
        )
    '''

    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()




def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

if __name__ == '__main__':
    main()

