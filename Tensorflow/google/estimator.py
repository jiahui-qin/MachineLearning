'''
tf.estimator是一种高级OOP API

'''

import tensorflow as tf
classifer = tf.estimator.LinearClassifier()
classifer.train(input_fn = train_input_fn, steps = 2000)
predictions = classifer.predict(input_fn = predict_input_fn)