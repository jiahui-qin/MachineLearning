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
        mz.append(float(i[0]))
        intensity.append(float(i[1]))    
print(mz)
print(intensity)##导入数据

x = tf.placeholder(tf.float32, [1,len(mz)])

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

hiddenDim = len(mz) - 1

W = weight_variable([hiddenDim, 1])
b = bias_variable([hiddenDim, 1])

W2 = weight_variable([1,hiddenDim])
b2 = bias_variable([1])

W3 = weight_variable([len(mz), len(mz)])
b3 = bias_variable([1,len(mz)])

hidden = tf.nn.sigmoid(tf.matmul(W, x)+b)
y = tf.matmul(W2, hidden+b2)

#min error
loss = tf.reduce_mean(tf.square(y - intensity))
step = tf.Variable(0, trainable=False)
rate = tf.train.exponential_decay(0.15, step, 1, 0.9999)
optimizer = tf.train.AdamOptimizer(rate)
train = optimizer.minimize(loss, global_step=step)
init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for time in range(0,10001):
    train.run({x: mz}, sess)
    if time % 1000  == 0:
        print('time', time, 'average loss',loss.eval({x: mz}))

