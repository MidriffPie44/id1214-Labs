import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np

import time
import random
import csv

import data_plot

num_heroes = 129  # not really but the hero id do not match
input_shape = num_heroes + num_heroes + 1  # plus one because 0 is not a hero id
hidden_shape = input_shape//2


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(input_shape, input_shape=(input_shape,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(hidden_shape, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(1, activation='linear', kernel_initializer=weights))

    model.compile(optimizers.Adam(), loss='mse')

    return model


def create_training_data(amount, min_medal=0, max_medal=1000, file='data.csv'):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = []
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]

            if min_medal <= match[-2] <= max_medal:
                data.append(match)

    raw_matches = random.sample(data, amount//2)

    sample = []
    label = []
    match_id = []
    for match in raw_matches:
        data_point_radiant = [0] * input_shape
        data_point_dire = [0] * input_shape

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


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


if __name__ == '__main__':
    print('Starting')
    t = time.time()

    data_samples, data_labels, match_ids = create_training_data(160000*2, min_medal=0, max_medal=100, file='data.csv')
    eval_samples, eval_labels, match_ids = create_training_data(5000*2, min_medal=0, max_medal=100, file='evaluation.csv')
    print('Generating training data:', time.time()-t)
    t = time.time()

    net = create_new_seq_model()
    print('Creating neural network:', time.time()-t)
    t = time.time()

    train_model(net, data_samples, data_labels, 100, 2000)
    print('Trained model:', time.time()-t)
    t = time.time()

    eval_predictions = predict_with_model(net, eval_samples)
    flat_raw_predictions = [prediction[0] for prediction in eval_predictions]
    flat_predictions = [int(round(prediction)) for prediction in flat_raw_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]

    print('Predictions:', flat_predictions[:100])
    print('Labels:\t\t', eval_labels[:100])
    print('accuracy:\t', accurate_predictions[:100])
    print('Accurate predictions:', sum(accurate_predictions))
    print('Inaccurate predictions:', len(eval_labels)-sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))
    print('Percentage:', sum(accurate_predictions)/len(eval_labels) * 100)

    max_index = flat_raw_predictions.index(max(flat_raw_predictions))
    min_index = flat_raw_predictions.index(min(flat_raw_predictions))

    print('max prediction:', match_ids[max_index], accurate_predictions[max_index], eval_labels[max_index], flat_raw_predictions[max_index])
    print('min prediction:', match_ids[min_index], accurate_predictions[min_index], eval_labels[min_index], flat_raw_predictions[min_index])
    
    rad_advantage = [data_labels[i] == data_samples[i][0] for i in range(len(data_samples))]
    print('radiant advantage:', sum(rad_advantage)/len(rad_advantage) * 100)

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 116, list(range(100)))
    data_plot.plot_accuracy(x_set, y_set, 'medal', 'accuracy')

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 115, list(range(6000)))
    data_plot.plot_accuracy(x_set, y_set, 'match duration', 'accuracy')

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 0, list(range(2)))
    data_plot.plot_accuracy(x_set, y_set, 'radiant', 'accuracy')

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 0, list(range(2)))
    data_plot.plot_accuracy(x_set, y_set, 'radiant', 'accuracy')




