import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np

import random
import csv

num_of_heroes = 129  # not really but the hero id do not match


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(num_of_heroes*2, input_shape=(num_of_heroes+2,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(num_of_heroes*4, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(num_of_heroes*4, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(num_of_heroes*4, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(num_of_heroes*4, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(1, activation='linear', kernel_initializer=weights))

    model.compile(optimizers.Adam(), loss='mse')

    return model


def create_training_data(amount):
    with open('data.csv', newline='') as f:
        reader = csv.reader(f)
        data = []
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]
            data.append(match)

    random_matches = [random.randint(0, len(data)-1) for _ in range(amount)]
    raw_matches = [data[match_num] for match_num in random_matches]

    sample = []
    label = []
    for match in raw_matches:
        data_point = [0] * (num_of_heroes + 2)
        for hero in match[1:11]:
            data_point[int(hero)] += 1
        data_point[-3] = match[-3]
        data_point[-2] = match[-2]
        sample.append(data_point.copy())

        label.append(match[-1])

    return sample, label


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


if __name__ == '__main__':
    data_samples, data_labels = create_training_data(15000)
    eval_samples, eval_labels = create_training_data(50)

    net = create_new_seq_model()

    train_model(net, data_samples, data_labels, 1000, 100)

    eval_predictions = predict_with_model(net, eval_samples)
    flat_predictions = [int(round(prediction[0])) for prediction in eval_predictions]

    print('Predictions:\t', flat_predictions)
    print('Labels:\t\t', eval_labels)
