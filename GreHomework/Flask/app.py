# -*- coding = utf-8 -*-
# @Time : 2022/6/21 15:46
# @Author : bai_zhou
# @File : app.py
# @Software : PyCharm

from flask import Flask, render_template
import sqlite3

import markdown
import importlib


app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def index1():
    return render_template("index.html")

@app.route("/book")
def book():
    datalist = []
    con = sqlite3.connect("../books.db")
    cur = con.cursor()
    sql = "select * from Book250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()

    return render_template("book.html", books = datalist)

@app.route("/score")
def score():
    score = []
    num = []
    con = sqlite3.connect("../books.db")
    cur = con.cursor()
    sql = "select score,count(score) from Book250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    con.close()
    return render_template("score.html", score = score, num = num)

@app.route("/wordcloud")
def wordcloud():
    return render_template("wordcloud.html")

@app.route("/clients")
def clients():
    return render_template("clients.html")

@app.route("/code")
def code():
    input_file = open("../mkd.md", mode="r", encoding="utf-8")
    text = input_file.read()
    mkd = markdown.markdown(text)
    return render_template("code.html")

@app.route("/test")
def test():
    return render_template("blog-details.html")

if __name__ == '__main__':
    app.run(debug=True)