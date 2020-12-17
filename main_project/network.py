import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np

import random
import csv

num_heroes = 129  # not really but the hero id do not match
added_data_points = 2
input_shape = num_heroes + num_heroes + added_data_points


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(input_shape, input_shape=(input_shape,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(input_shape * 2, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(input_shape * 2, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(input_shape * 2, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(input_shape * 2, activation='relu', kernel_initializer=weights))
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
        data_point_win = [0] * input_shape
        data_point_loss = [0] * input_shape

        for allied_hero in match[1:6]:
            data_point_win[int(allied_hero)] += 1
            data_point_loss[int(allied_hero) + num_heroes] += 1

        for enemy_hero in match[6:11]:
            data_point_win[int(enemy_hero) + num_heroes] += 1
            data_point_loss[int(enemy_hero)] += 1

        data_point_win[-3] = match[-3]  # duration
        data_point_win[-2] = match[-2]  # rank
        data_point_loss[-3] = match[-3]  # duration
        data_point_loss[-2] = match[-2]  # rank

        sample.append(data_point_win.copy())
        sample.append(data_point_loss.copy())
        label.append(match[-1])  # for win
        label.append(int(not match[-1]))  # for loss

    return sample, label


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


if __name__ == '__main__':
    data_samples, data_labels = create_training_data(10000)
    eval_samples, eval_labels = create_training_data(50)

    net = create_new_seq_model()

    train_model(net, data_samples, data_labels, 100, 100)

    eval_predictions = predict_with_model(net, eval_samples)
    flat_predictions = [int(round(prediction[0])) for prediction in eval_predictions]
    #flat_predictions = [prediction[0] for prediction in eval_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]

    print('Predictions:', flat_predictions)
    print('Labels:\t\t', eval_labels)
    print('accuracy:\t', accurate_predictions)
    print('Accurate predictions:', sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))
