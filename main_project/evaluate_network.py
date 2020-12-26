import keras.layers as layers
import keras.optimizers as optimizers
import keras.models as models
from keras import Sequential
import numpy as np

import time
import random
import csv

from data_plot import generate_plot_data as data
from data_plot import plot_accuracy as plot
import train_network

num_heroes = 129  # not really but the hero id do not match
input_shape = num_heroes + num_heroes + 1  # plus one because 0 is not a hero id
hidden_shape = input_shape//2


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


if __name__ == '__main__':
    print('Starting')
    t = time.time()

    eval_samples, eval_labels, match_ids = train_network.create_training_data(20000 * 2, file='evaluation.csv')
    print('Generating training data:', time.time() - t)
    t = time.time()

    net = models.load_model('net_26_12')
    print('Loaded neural network:', time.time() - t)
    t = time.time()

    raw_prediction = predict_with_model(net, eval_samples)
    flat_raw_predictions = [prediction[0] for prediction in raw_prediction]
    flat_predictions = [int(round(prediction)) for prediction in flat_raw_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]

    print('Predictions:', flat_predictions[:100])
    print('Labels:\t\t', eval_labels[:100])
    print('accuracy:\t', accurate_predictions[:100])
    print('Accurate predictions:', sum(accurate_predictions))
    print('Inaccurate predictions:', len(eval_labels) - sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))
    print('Percentage:', sum(accurate_predictions) / len(eval_labels) * 100)

    max_index = flat_raw_predictions.index(max(flat_raw_predictions))
    min_index = flat_raw_predictions.index(min(flat_raw_predictions))

    print('max prediction:', match_ids[max_index], accurate_predictions[max_index], flat_raw_predictions[max_index])
    print('min prediction:', match_ids[min_index], accurate_predictions[min_index], flat_raw_predictions[min_index])

    rad_advantage = [eval_labels[i] == eval_samples[i][0] for i in range(len(eval_labels))]
    print('radiant advantage:', sum(rad_advantage) / len(rad_advantage) * 100)

    x_set, y_set, volume = data(eval_samples, eval_labels, flat_predictions, 116, range(0, 100, 4), 2)
    plot(x_set, y_set, volume, 'medal', 'accuracy')

    x_set, y_set, volume = data(eval_samples, eval_labels, flat_predictions, 115, range(15*60, 60*60, 3*60), 3*30)
    plot(x_set, y_set, volume, 'match duration, seconds', 'accuracy')

    x_set, y_set, volume = data(eval_samples, eval_labels, flat_predictions, 0, range(2))
    plot(x_set, y_set, volume, 'radiant', 'accuracy')

    percentage_prediction = [[int(round(prediction * 100))] for prediction in flat_raw_predictions]
    x_set, y_set, volume = data(percentage_prediction, eval_labels, flat_predictions, 0, range(-50, 150, 5), 2.5)
    plot(x_set, y_set, volume, 'prediction', 'accuracy')

    prediction_deviation = [[abs(prediction[0] - 50)] for prediction in percentage_prediction]
    x_set, y_set, volume = data(prediction_deviation, eval_labels, flat_predictions, 0, range(0, 150, 5), 2.5)
    plot(x_set, y_set, volume, 'deviation', 'accuracy')
