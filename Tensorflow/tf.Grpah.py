"""
Tensorflow的计算需要定义图中所有的计算，然后执行计算
tensorflow支持使用tf.Graph函数生成新的计算图
不同计算图上的张量和运算不会共享
这是一个示例，用tensorflow来拟合示例数据
"""
import tensorflow as tf
import numpy as np

##生成示例数据，y_data = x_data*0.1 + 0.3
x_data = np.random.rand(100).astype("float32")
y_data = x_data*0.1 + 0.3

#生成变量，拟合y方程
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
y = W * x_data + b

#定义损失函数train
loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#初始化变量，示例里边用的是.initialize_all_variables()，已经被弃用
init = tf.global_variables_initializer()

#启动这个图
sess = tf.Session()
sess.run(init)

#拟合
for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(W), sess.run(b))

##最后有一个小tips，pylint里的错误c0103：constant的名字开头应该用大写字母，variable的开头应该用小写字母