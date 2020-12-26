import keras.layers as layers
import keras.optimizers as optimizers
import keras.models as models
from keras import Sequential
import numpy as np

import time
import random
import csv

import data_plot
import train_network

num_heroes = 129  # not really but the hero id do not match
input_shape = num_heroes + num_heroes + 1  # plus one because 0 is not a hero id
hidden_shape = input_shape//2



if __name__ == '__main__':
    print('Starting')
    t = time.time()

    eval_samples, eval_labels, match_ids = train_network.create_training_data(20000 * 2, min_medal=0, max_medal=100, file='evaluation.csv')
    print('Generating training data:', time.time() - t)
    t = time.time()

    net = models.load_model()
    print('Loaded neural network:', time.time() - t)
    t = time.time()

    eval_predictions = train_network.predict_with_model(net, eval_samples)
    flat_raw_predictions = [prediction[0] for prediction in eval_predictions]
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

    print('max prediction:', match_ids[max_index], accurate_predictions[max_index], eval_labels[max_index],
          flat_raw_predictions[max_index])
    print('min prediction:', match_ids[min_index], accurate_predictions[min_index], eval_labels[min_index],
          flat_raw_predictions[min_index])

    rad_advantage = [eval_labels[i] == eval_labels[i][0] for i in range(len(eval_labels))]
    print('radiant advantage:', sum(rad_advantage) / len(rad_advantage) * 100)

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 116, list(range(100)))
    data_plot.plot_accuracy(x_set, y_set, 'medal', 'accuracy')

    x_set, y_set = data_plot.duration_data(eval_samples, eval_labels, flat_predictions, 115, list(range(15, 120)))
    data_plot.plot_accuracy(x_set, y_set, 'match duration', 'accuracy')

    x_set, y_set = data_plot.generate_plot_data(eval_samples, eval_labels, flat_predictions, 0, list(range(2)))
    data_plot.plot_accuracy(x_set, y_set, 'radiant', 'accuracy')

    percentage_prediction = [[int(round(prediction * 100))] for prediction in flat_raw_predictions]
    x_set, y_set = data_plot.generate_plot_data(percentage_prediction, eval_labels, flat_predictions, 0,
                                                list(range(120)))
    data_plot.plot_accuracy(x_set, y_set, 'prediction', 'accuracy')

    prediction_deviation = [[abs(prediction[0] - 50)] for prediction in percentage_prediction]
    x_set, y_set = data_plot.generate_plot_data(prediction_deviation, eval_labels, flat_predictions, 0,
                                                list(range(120)))
    data_plot.plot_accuracy(x_set, y_set, 'deviation', 'accuracy')