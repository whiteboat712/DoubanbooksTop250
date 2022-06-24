# -*- coding = utf-8 -*-
# @Time : 2022/6/23 10:08
# @Author : bai_zhou
# @File : wordcloudprint.py
# @Software : PyCharm

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image
import numpy as np
import sqlite3


con = sqlite3.connect('../books.db')
cur = con.cursor()
sql = 'select instruction from Book250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
cur.close()
con.close()

cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))


img = Image.open(r'static/file/picture.png')
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    width=4000,
    height=2000,
    mask=img_array,
    max_font_size=None,
    font_path="msyh.ttc",
    contour_width=8,
    contour_color='#66ccff'
)
wc.generate_from_text(string)


fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')

plt.savefig(r'static/file/word.png',dpi=800)