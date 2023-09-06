import tensorflow as tf
print("tf.__version__: ", tf.__version__)
mnist = tf.keras.datasets.mnist
# 关于minist数据, https://doc.codingdict.com/tensorflow/tfdoc/tutorials/mnist_download.html
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0