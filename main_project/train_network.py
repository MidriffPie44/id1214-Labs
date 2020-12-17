import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np

import time
import random
import csv

num_heroes = 129  # not really but the hero id do not match
added_data_points = 3
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


def create_training_data(amount, min_medal=0, max_medal=1000, evaluation=False):
    if evaluation:
        file = 'evaluation.csv'
    else:
        file = 'data.csv'

    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = []
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]

            if min_medal <= match[-2] <= max_medal:
                data.append(match)

    raw_matches = []
    while len(raw_matches) < amount // 2:
        random_match_num = random.randint(0, len(data) - 1)
        raw_matches.append(data[random_match_num])

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

        data_point_radiant[-3] = match[-3]  # duration
        data_point_radiant[-2] = match[-2]  # rank
        data_point_radiant[-1] = 1  # team is radiant
        data_point_dire[-3] = match[-3]  # duration
        data_point_dire[-2] = match[-2]  # rank
        data_point_dire[-1] = 0  # team is not radiant

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

    data_samples, data_labels, _ = create_training_data(10000, min_medal=0, max_medal=100)
    eval_samples, eval_labels, match_ids = create_training_data(100, min_medal=0, max_medal=100, evaluation=True)
    print('Generating training data:', time.time()-t)
    t = time.time()

    net = create_new_seq_model()
    print('Creating neural network:', time.time()-t)
    t = time.time()

    train_model(net, data_samples, data_labels, 1000, 1000)
    print('Trained model:', time.time()-t)
    t = time.time()

    eval_predictions = predict_with_model(net, eval_samples)
    flat_predictions = [int(round(prediction[0])) for prediction in eval_predictions]
    #flat_predictions = [prediction[0] for prediction in eval_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]
    eval_correct_predictions = []
    for i in range(len(eval_predictions)):
        print(accurate_predictions[i], eval_labels[i], eval_predictions[i][0], match_ids[i])

    print('Predictions:', flat_predictions)
    print('Labels:\t\t', eval_labels)
    print('accuracy:\t', accurate_predictions)
    print('Accurate predictions:', sum(accurate_predictions))
    print('Inaccurate predictions:', len(eval_labels)-sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))

    print('sum correct predictions:', sum(abs(x-0.5) * y for x, y in zip(eval_predictions, accurate_predictions))[0])
    print('sum incorrect predictions:', sum(abs(x-0.5) * int(not y) for x, y in zip(eval_predictions, accurate_predictions))[0])

    net.save('network.net')
