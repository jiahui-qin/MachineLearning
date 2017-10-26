# Tensorflow 使用基础

* 使用 graph 来表示计算,graph中的节点称为op(operation)
* 在 session 中执行图，计算开始前，graph必须在Session中被启动
* 使用 tensors 来代表数据，Python中返回numpy的ndarry对象
* 通过 variables 维护状态
* 使用 feeds & fetchs 将数据传入或传出任何操作

## The computation graph

Tensorflow变成可以按两个阶段组织起来：
1.construction，构建阶段，用来组织计算图
2.execution，执行阶段，利用session中执行计算图中的op操作

### building the graph

刚开始基于op建立图时一般不需要输入源。Python库中的op构造函数可以返回op作为输出对象，这些op可以作为其他op构造函数作为输入

    import tensorflow as tf
    matrix1 = tf.constant([[3., 3.]])
    matrix2 = tf.constant([[2.], [2.]])
    # 创建了一个 Matmul op，返回一个乘法运算
    product = tf.matmul(matrix1, matrix2)

### Launching the graph in a session

想要执行一个图，必须先创建一个Session
    
    sess = tf.Session()
    result = sess.run(product)
    print(result)
    sess.close()
也可以使用一个with，自动关闭：
    
    with tf.Session as sess:
        result = sess.run([product])
        print(result)
*python中with语句的使用需要支持Context Management Protocol，即包含方法 \_\_enter\_\_() 和 \_\_exit\_\_(),Session对象好像没有这两个方法，在test文件中并不能使用with语句，这里还是建议使用sess.close()方法 [参考文章](https://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/)*
    
    tf.device("/gpu:1") #可以指定调用第几个gpu，此处应该有一个退出语句，建议使用with

### Tensors

使用tensors数据结构来代表所有的数据，可以把tensors看作一个n维的数组或列表，一个tensor包可以一个rank，和一个shape

### Variables

tf.assign(ref, value)可以使用value来更新ref的值。通常会将一个统计模型中的参数表示为一组变量. 例如,可以将一个神经网络的 权重作为某个变量存储在一个 tensor 中. 在训练过程中, 通过重复运行训练图, 更新这个 tensor.
    
    import tensorflow as tf
    state = tf.Variable(0, name="counter")
    one = tf.constant(1)
    new_value = tf.add(state, one)
    update = tf.assign(state, new_value)
    init_op = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init_op)
    print(sess.run(state))
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))
    sess.close()

### Fetchs

可以在使用Session()的run()调用执行图时，传入多个tensor，这些tensor可以取回结果，需要获取的多个 tensor 值，应该在op的一次运行中获取
    
    sess.run([update, one]) # 当然这里取回one没有意义

### Feeds

feed机制：可以临时代替图中的任意操作中的tensor，可以对图中的任何操作提交补丁，直接插入一个tensor

你可以提供 feed 数据作为 run() 调用的参数.feed 只在调用它的方法内有效, 方法结束, feed 就会消失. 最常见的用 例是将某些特殊的操作指定为"feed" 操作, 标记的方法是使用tf.placeholder()为这些操作创建占位符
    
    import tensorflow as tf
    input1 = tf.placeholder(tf.float32)
    input2 = tf.placeholder(tf.float32)
    output = tf.multiply(input1, input2)
    sess = tf.Session()
    print(sess.run([output], feed_dict={input1:[7.], input2:[2.]})) 
    sess.close()


