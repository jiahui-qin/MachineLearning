## http://www.toutiao.com/a6470402811564655118/?tt_from=copy_link&utm_campaign=client_share&app=news_article_social&utm_source=copy_link&iid=15210768190
import csv
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
mz = []
intensity = []

with open('F:\\MS\\test.csv', 'r') as csvfile:
    read = csv.reader(csvfile)
    for i in read:
        mz.append(i[0])
        intensity.append(i[1])       
print(mz)
print(intensity)##导入数据

x = tf.placeholder(tf.float21, [1,len(mz)])

