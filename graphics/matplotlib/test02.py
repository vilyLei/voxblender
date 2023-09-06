# pip uninstall tensorflow
# pip install --upgrade --ignore-installed tensorflow
import tensorflow as tf
import keras
from tensorflow.keras import layers

print("keras.__version__: ",keras.__version__)
print("tf.__version__: ", tf.__version__)
# print(tf.keras.__version__)
# print(tf.keras)
tf.compat.v1.Session()

# thanks: https://zhuanlan.zhihu.com/p/58825020
model = tf.keras.Sequential()
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

# thanks: https://www.tensorflow.org/tutorials/quickstart/beginner?hl=zh-cn
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0