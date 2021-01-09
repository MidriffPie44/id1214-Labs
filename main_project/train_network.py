import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np

import time
import random
import csv


num_heroes = 129  # not really but the hero id do not match
input_shape = num_heroes + num_heroes + 1  # plus one because 0 is not a hero id
hidden_shape = input_shape//3 * 2


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(input_shape, input_shape=(input_shape,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))  # 3 hidden layers was tested
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))  # to be the best number of
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))  # layers
    model.add(layers.Dense(1, activation='linear', kernel_initializer=weights))

    model.compile(optimizers.Adam(), loss='mse')

    return model


def create_training_data(amount, min_medal=0, max_medal=1000, file='data.csv'):
    with open(file, newline='') as f:  # reads all the data from the file
        reader = csv.reader(f)
        data = []
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]

            if min_medal <= match[-2] <= max_medal:
                data.append(match)

    raw_matches = random.sample(data, amount//2)  # pick a specified number of matches randomly from the full data list

    sample = []
    label = []
    match_id = []
    for match in raw_matches:
        data_point_radiant = [0] * input_shape  # Each match is processed twice, once from the perspective of the losing
        data_point_dire = [0] * input_shape     # and once from the perspective of the winning team.

        for allied_hero in match[1:6]:
            data_point_radiant[int(allied_hero)] += 1
            data_point_dire[int(allied_hero) + num_heroes] += 1

        for enemy_hero in match[6:11]:
            data_point_radiant[int(enemy_hero) + num_heroes] += 1
            data_point_dire[int(enemy_hero)] += 1

        data_point_duration = 115  # this is not a hero id so it is used as duration
        data_point_rank = 116  # this is also not a hero id so is used as rank

        data_point_radiant[data_point_duration] = match[-3]  # duration
        data_point_radiant[data_point_rank] = match[-2]  # rank
        data_point_radiant[0] = 1  # team is radiant
        data_point_dire[data_point_duration] = match[-3]  # duration
        data_point_dire[data_point_rank] = match[-2]  # rank
        data_point_dire[0] = 0  # team is not radiant

        sample.append(data_point_radiant.copy())
        sample.append(data_point_dire.copy())
        label.append(match[-1])  # for win
        label.append(int(not match[-1]))  # for loss
        match_id.append(match[0])
        match_id.append(match[0])

    return sample, label, match_id


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


if __name__ == '__main__':
    model_name = ''
    while not model_name:
        model_name = input('Enter name of new model:')

    t = time.time()

    print('Starting')
    data_samples, data_labels, match_ids = create_training_data(1500000*2, min_medal=0, max_medal=100, file='data.csv')
    eval_samples, eval_labels, _ = create_training_data(10000, min_medal=0, max_medal=100, file='evaluation.csv')
    print('Generating training data:', time.time()-t)
    t = time.time()

    net = create_new_seq_model()
    print('Creating neural network:', time.time()-t)
    t = time.time()

    train_model(net, data_samples, data_labels, 250, 1000)
    print('Trained model:', time.time()-t)
    t = time.time()

    net.save(model_name)
    print('Saved model:', time.time() - t)
    t = time.time()

    raw_eval_prediction = predict_with_model(net, eval_samples)
    flat_eval_predictions = [prediction[0] for prediction in raw_eval_prediction]
    flat_predictions = [int(round(prediction)) for prediction in flat_eval_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]

    print('Predictions:\t', flat_predictions[:50])
    print('Labels:\t\t', eval_labels[:50])
    print('accuracy:\t', accurate_predictions[:50])
    print('Accurate predictions:', sum(accurate_predictions))
    print('Inaccurate predictions:', len(eval_labels)-sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))
    print('Percentage:', sum(accurate_predictions)/len(eval_labels) * 100)
