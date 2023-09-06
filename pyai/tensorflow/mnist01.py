## base on tensorflow version 2.0+
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets,layers,optimizers
import matplotlib
from matplotlib import pyplot as plt

### 定义预处理函数preprocess
def preprocess(x,y):
    print(x.shape,y.shape)
    x = tf.cast(x,dtype=tf.float32)/255.    #把图片中的灰度值归一化到0~1区间
    x = tf.reshape(x,[-1,28*28])            #把每一张图片都打平成28*28的一维向量，方便神经网络模型处理
    y = tf.cast(y,dtype=tf.int32)           #把训练集中的标签值类型转化为tf.int32类型
    y = tf.one_hot(y,depth=10)              #然后把标签值处理为one_hot编码格式的数据    
    return x,y

print("tf.__version__: ", tf.__version__)
print("matplotlib.__version__: ", matplotlib.__version__)
### 加载mnist数据集
(x_train,y_train),(x_test,y_test) = datasets.mnist.load_data()
print('x_train:',x_train.shape,'y_train:',y_train.shape,'x_test:',x_test.shape,'y_test:',y_test.shape)
# 输出结果如下:
# x_train: (60000, 28, 28)
# y_train: (60000,)
# x_test: (10000, 28, 28)
# y_test: (10000,)

#### 把训练集和测试集做成一个Tensorflow易于批量处理的Dataset
batchsz = 512                           # 批量处理大小，表示一次性可以处理512张图片

### 处理训练集
train_db = tf.data.Dataset.from_tensor_slices((x_train,y_train))
train_db = train_db.shuffle(1000)       # 把训练集中的数据打散，防止神经网络记忆住训练数据
train_db = train_db.batch(batchsz)      # 批量化处理
train_db = train_db.map(preprocess)     # 对训练数据集中的数据做预处理
train_db = train_db.repeat(20)          # 对整个训练数据集遍历20次进行训练

### 处理测试集合
test_db = tf.data.Dataset.from_tensor_slices((x_test,y_test))
test_db = test_db.batch(batchsz)
test_db = test_db.map(preprocess)

# 查看批量处理后，训练集中的数据
sample_x,sample_y = next(iter(train_db))
print(sample_x.shape,sample_y.shape)
# 输出结果如下:
# (512, 784)
# (512, 10)
def main():
    lr = 1e-2                           # 学习率
    losses,accs = [],[]                 # 用来保存损失值和准确率的数组
    
    # 初始化模型需要用到的超参数
    w1,b1 = tf.Variable(tf.random.normal([784,256],stddev=0.1)),    tf.Variable(tf.zeros([256]))
    w2,b2 = tf.Variable(tf.random.normal([256,128],stddev=0.1)),    tf.Variable(tf.zeros([128]))
    w3,b3 = tf.Variable(tf.random.normal([128,10],stddev=0.1)),     tf.Variable(tf.zeros([10]))

    # 使用一个for循环进行迭代20次
    for step, (x,y) in enumerate(train_db):
        with tf.GradientTape() as tape:
            # 下面这个是用张量实现的一个简单的全连接层
            h1 = x@w1+b1
            h1 = tf.nn.relu(h1)         # 激活函数采用relu函数

            h2 = h1@w2+b2
            h2 = tf.nn.relu(h2)

            out = h2@w3+b3
    
            loss = tf.square(y-out)     # 这里是每一张图片的损失值
            loss = tf.reduce_mean(loss) # 计算这批样本的损失值的均值
            
        grads = tape.gradient(loss,[w1,b1,w2,b2,w3,b3])     # 根据损失值计算出各个超参数的梯度
        for p,g in zip([w1,b1,w2,b2,w3,b3],grads):
            p.assign_sub(g*lr)                              # 对超参数进行梯度下降
    
        # 训练100步后打印损失值
        if step%100 ==0:
            print(step,'loss:',float(loss))
            losses.append(float(loss))
            
        if step%100 ==0:
            # 每训练100次后，测试模型
            total,total_correct = 0.,0.
            for x_test,y_test in test_db:
                h1 = x_test@w1+b1
                h1 = tf.nn.relu(h1)
                
                h2 = h1@w2+b2
                h2 = tf.nn.relu(h2)
                
                out = h2@w3+b3
                
                pred = tf.argmax(out,axis=1)                # 测试集的预测值
                y_test = tf.argmax(y_test,axis=1)           # 测试集的真实标签
                
                correct = tf.equal(y_test,pred)             # 计算预测正确的数据
                total_correct += tf.reduce_sum(tf.cast(correct,dtype=tf.int32)).numpy()
                total += y_test.shape[0]
                
            print(step, 'Evaluate acc:', total_correct/total)
            accs.append(total_correct/total)
    
    # 画模型的训练误差曲线
    plt.figure()
    x = [i*80 for i in range(len(losses))]
    plt.plot(x,losses,color='C0',marker='s',label='训练')
    plt.xlabel('Step')
    plt.ylabel('MSE')
    plt.legend()
    plt.savefig('train.svg')
    
    # 画模型的测试准确率曲线
    plt.figure()
    plt.plot(x,accs,color='C1',marker='s',label='测试')
    plt.xlabel('Step')
    plt.ylabel('准确率')
    plt.legend()
    plt.savefig('test.svg')

if __name__ == '__main__':
    main()