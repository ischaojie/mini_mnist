import logging
import os

import tensorflow as tf
from tensorflow import keras

logging.basicConfig(level=logging.INFO)
base_path = os.path.abspath(os.path.dirname(__file__))
logging.info('base path: {}'.format(base_path))

# 导入数据集
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

train_images = train_images.reshape(-1, 28 * 28) / 255.0
test_images = test_images.reshape(-1, 28 * 28) / 255.0


# 构建模型
def create_model():
    model = keras.Sequential([
        keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    # 编译模型
    model.compile(
        # 优化器：模型更新方式
        optimizer='adam',
        # 损失函数：函数最小化，以拟合
        loss='sparse_categorical_crossentropy',
        # 评价方式
        metrics=['accuracy']
    )

    return model


model = create_model()
model.summary()

model.fit(train_images, train_labels, epochs=5)
# 保存整个model
# 包括权重，模型的结构，优化器配置
model.save('mnist_model.h5')
