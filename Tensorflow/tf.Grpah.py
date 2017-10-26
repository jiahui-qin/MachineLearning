"""
Tensorflow的计算需要定义图中所有的计算，然后执行计算
tensorflow支持使用tf.Graph函数生成新的计算图
不同计算图上的张量和运算不会共享
"""
import tensorflow as tf

g1 = tf.Graph()
with g1.as_default():
    v = tf.get_variable("v",initializer=tf.zeros_initializer(shape=[1]))

g2 = tf.Graph()
with gl.as_default():
    v = tf.get_variable("v",initializer=tf.ones_initializer(shape=[1]))

with tf.Session(graph = g1) as sess:
    tf.initialize_all_veriables().run()
    with tf.variable_scope("", ruse=True):
        print(sess.run(tf.get_variable("v")))

with tf.Session(graph = g2) as sess:
    tf.initialize_all_veriables().run()
    with tf.variable_scope("", ruse=True):
        print(sess.run(tf.get_variable("v")))
