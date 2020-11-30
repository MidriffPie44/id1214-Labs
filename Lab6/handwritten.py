import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np
import random

import csv


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(50, input_shape=(28*28,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(50, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(10, activation='linear', kernel_initializer=weights))

    model.compile(optimizers.Adam(), loss='mse')

    return model


def create_training_data(amount):
    with open('handwritten_digits/train.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[1:amount+1]

    raw_sample = [image[1:785] for image in data]
    sample = []
    for image in raw_sample:
        sample.append([int(pixel) for pixel in image])

    raw_labels = [image[0] for image in data]
    label = [[0 for i in range(10)] for j in range(amount)]
    for i in range(amount):
        image_label = int(raw_labels[i])
        label[i][image_label] = 1

    return sample, label


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


if __name__ == '__main__':
    data_samples, data_labels = create_training_data(40000)
    #print(data_samples)
    #print(data_labels)
    eval_samples, eval_labels = create_training_data(100)

    net = create_new_seq_model()

    train_model(net, data_samples, data_labels, 1000, 1000)

    eval_predictions = predict_with_model(net, eval_samples)

    eval_predictions = [list(predictions) for predictions in eval_predictions]
    eval_labels = [list(labels) for labels in eval_labels]

    print('Predictions:\t', [eval_prediction.index(max(eval_prediction)) for eval_prediction in eval_predictions])
    print('Labels:\t\t\t', [eval_label.index(max(eval_label)) for eval_label in eval_labels])



