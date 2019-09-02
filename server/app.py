import logging
import os

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from tensorflow import keras

logging.basicConfig(level=logging.INFO)
base_path = os.path.abspath(os.path.dirname(__file__))
logging.info('base path: {}'.format(base_path))

app = Flask(__name__)
CORS(app)


def proprecess(figure):
    predict_image = np.array(figure)
    predict_image = np.expand_dims(predict_image, axis=0)
    predict_image = predict_image.reshape(-1, 28 * 28) / 255.0
    logging.info('image shape: {}'.format(predict_image.shape))

    return predict_image


def predict(figure):
    model = keras.models.load_model(os.path.join(base_path, 'mnist_model.h5'))
    logging.info('模型记载完成...')
    prediction = model.predict(proprecess(figure))
    logging.info('预测结果: {}'.format(prediction))
    return np.argmax(prediction[0])


@app.route('/', methods=['GET'])
def index():
    return jsonify('this is mini mnist api.')


@app.route('/predict', methods=['GET', 'POST'])
def mnist():
    figure = request.args.get('figure', '')

    if figure != '':
        figure = eval(figure)
        figure = [v for v in figure['input'].values()]
        result = predict(figure)
        return jsonify(label=str(result))
    return jsonify('no data.')


if __name__ == '__main__':
    app.run(debug=True)
