#http://www.tensorfly.cn/tfdoc/tutorials/mnist_pros.html minist数据集测试，tensorflow入门
import input_data 
#这里导入数据的时候导入不进来，修改了一下input_data文件，不用在网络上下载直接读取下载在本地的文件
#Download the file from http://yann.lecun.com/exdb/mnist/
#修改了38行和去掉了maybe_download函数
minst = input_data.read_data_sets("MINST_data/", one_hot = True)
##softmax回归 首先对输入的对象属于某个类的证据进行求和，然后将这个证据的和转化为概率
import tensorflow as tf
sess = tf.InteractiveSession()
x = tf.placeholder("float", shape = [None, 784])
y_ = tf.placeholder("float", shape = [None, 10])

##定义模型权重W和偏置b,都初始化为0向量
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
#变量需要通过session初始化之后才可以在session中使用
sess.run(tf.global_variables_initializer())

#定义回归模型和损失函数，这里回归模型用的是softmax，损失函数是目标类别和预测类别之间的交叉熵
y = tf.nn.softmax(tf.matmul(x,W) + b)
cross_entroy = 0 - tf.reduce_sum(y_ * tf.log(y))

#训练模型，最速下降法
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entroy)
for i in range(1000):
    batch = minst.train.next_batch(50)
    train_step.run(feed_dict = {x:batch[0], y_:batch[1]})

#评估模型,tf.argmax给出某个tensor对象在其某一维上的其数据最大值所在的索引，这里索引就代表了其匹配的结果
#所以用其tf.equal来检测我们的预测是否和真实标签匹配
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(accuracy.eval(feed_dict = {x: minst.test.images, y_:minst.test.labels}))
##最后训练的准确率是90.92%
print('__________________________________________')
print('构建一个多层卷积网络')
print('__________________________________________')

##使用卷积神经网络来改善效果
##权重用少量的噪声，std=0.1，用一个较小的证书初始化偏置项，0.1
##这里就定义了两个函数用于初始化
def weight_variable(shape):
    inital = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(inital)

def bias_variable(shape):
    inital = tf.constant(0.1, shape = shape)
    return tf.Variable(inital)

##卷积和池化
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides = [1, 1, 1, 1], padding = 'SAME')
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')

#第一层卷积
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,28,28,1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

#第二层卷积
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

#密集连接层
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

#Dropout减少过拟合
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

#输出层
W_fc2 = weight_variable([1024,10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2) + b_fc2)

#训练与评估模型
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
sess.run(tf.global_variables_initializer())
for i in range(20000):
  batch = minst.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0})
    print( "step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print( "test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))