# tensorflow运作方式

## 构建图表：

1. inference()尽可能的构建好图表

2. loss()往inference图表中添加生成损失(loss)所需要的操作(ops)

3. training()往损失图表中添加计算并应用梯度(gradients)所需要的操作

![avator](http://www.tensorfly.cn/tfdoc/images/mnist_subgraph.png)

### 推理(inference)
    def inference(images, hidden1_units, hidden2_units):
    """
    Build the MNIST model up to where it may be used for inference.

    Args:
      images: Images placeholder, from inputs().
      hidden1_units: Size of the first hidden layer.
      hidden2_units: Size of the second hidden layer.

    Returns:
      softmax_linear: Output tensor with the computed logits.
    """
    # Hidden 1
    with tf.name_scope('hidden1'):
      weights = tf.Variable(
          tf.truncated_normal([IMAGE_PIXELS, hidden1_units],
                              stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))),
          name='weights')
      biases = tf.Variable(tf.zeros([hidden1_units]),
                           name='biases')
      hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)
    # Hidden 2
    with tf.name_scope('hidden2'):
      weights = tf.Variable(
          tf.truncated_normal([hidden1_units, hidden2_units],
                              stddev=1.0 / math.sqrt(float(hidden1_units))),
          name='weights')
      biases = tf.Variable(tf.zeros([hidden2_units]),
                           name='biases')
      hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)
    # Linear
    with tf.name_scope('softmax_linear'):
      weights = tf.Variable(
          tf.truncated_normal([hidden2_units, NUM_CLASSES],
                              stddev=1.0 / math.sqrt(float(hidden2_units))),
          name='weights')
      biases = tf.Variable(tf.zeros([NUM_CLASSES]),
                           name='biases')
      logits = tf.matmul(hidden2, weights) + biases
    return logits

tf.name_scope('前缀')使创建于该作用域之下的所有元素都带其前缀，上边的inference函数生成了hidden1\hidden2\linear三层，对每一层都生成了其权重、bias

对于权重变量。用tf.truncated_normal()生成，正态分布，首先是一个二维数组shape作为输入变量，第一个维度代表该层权重变量所连接(connect from)的单元数量，第二个维度代表该层权重所连接到(connect to)的单元数量。这个函数使用维度和标准差生成一个二维随机变量

对于bias，用tf.zeros生成，shape就是该层connect to到的单元数量

图表的3个主要操作，是两个tf.nn.relu激活函数，*tf.nn.relu(tf.matmul(images, weights) + biases)*,嵌入了隐藏层所需的tf.matmul矩阵相乘操作，最后返回logits模型所需要的另外一个tf.matmul，三者依次生成。

### 损失LOSS
labels_placeholder中的值被编码为一个表示识别出来的结果的一维向量

    batch_size = tf.size(labels)
    labels = tf.expand_dims(labels, 1)
    indices = tf.expand_dims(tf.range(0, batch_size, 1), 1)
    concated = tf.concat(1, [indices, labels])
    onehot_labels = tf.sparse_to_dense(concated, tf.pack([batch_size, NUM_CLASSES]), 1.0, 0.0)

tf.nn.softmax_cross_entropy_with_logits操作比较inference()函数与onehot_labels标签输出的logits Tensor

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits,onehot_labels,name='xentropy')

然后用tf.reduce_mean韩式计算batch维度下交叉熵的平均值，将该值作为总loss

    loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')

[交叉熵](http://colah.github.io/posts/2015-09-Visual-Information/)

### 训练TRAINING

使用梯度下降将损失函数最小化

首先从loss()中获取损失tensor，将其交给tf.scalar_summary()。配合SummaryWriter可以向事件文件中生成汇总值，在本篇中，每次出写入汇总值，都会释放损失tensor的当前值

    tf.scalar_summary(loss.op.name, loss)

然后实例化一个tf.train.GradientDescentOptimizer，按照要求的学习效率应用梯度下降法

    optimizer = tf.train.GradientDescentOptimizer(FLAGS, learning_rate)

然后生成一个变量用于保存glibal training step的数值，并使用minimize()函数更新系统中的triangle weights(*这里应该是inference步骤中的三个权重？*),这个操作称为train_op

    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)

最后返回包含了train_op输出结果的tensor

## 训练模型

### 图表

    with tf.Graph().as_defalut()

将构建的操作与默认的tf.Graph全局实例关联起来

### 会话

创建一个tf.Session()，可以用with语句生成，限制作用于，没有传入参数时该代码依附于默认的本地会话

    with tf.Session() as sess:

使用下列语句来初始化变量，传入参数

    init = tf.initialize_all_variables()
    sess.run(init)

### 训练循环

最简单的训练循环：
    for step in xrange(max_steps):
        sess.run(train_op)

### 向图表提供反馈

每执行一步，会生成一个feed dictionary,包含对于步骤中训练所要使用的例子，这些离子的hash key就是其所代表的占位符操作

    images_feed, labels_feed = data_set.next_batch(FLAGS.batch_size)

    feed_dict = {images_placeholder: images_feed,labels_placeholder: labels_feed,}

这个字典作为feed_dict参数传入sess.run函数

### 检查状态
    for step in xrange(FLAGS.max_steps):
        feed_dict = fill_feed_dict(data_sets.train,images_placeholder,labels_placeholder)
        _, loss_value = sess.run([train_op, loss], feed_dict=feed_dict)

获取loss

### 状态可视化
[tensorboard](http://www.tensorfly.cn/tfdoc/how_tos/summaries_and_tensorboard.html)

### 保存检查点

在训练中定期使用saver = tf.train.Saver(),调用saver.save()向训练文件夹中写入当前可训练变量中值得检查的文件，检查时可以使用saver.restore()来重载模型的参数

### 评估模型

每隔一千个训练步骤，我们的代码会尝试使用训练数据集与测试数据集，对模型进行评估。do_eval函数会被调用三次，分别使用训练数据集、验证数据集合测试数据集。

### 构建评估图表EVAL GRAPH

###评估图表的输出 EVAL OUTPUT
