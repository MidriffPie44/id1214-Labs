import keras.models as models
import numpy as np

import matplotlib.pyplot as plt
import time

import train_network


num_heroes = 129  # not really but the hero id do not match
input_shape = num_heroes + num_heroes + 1  # plus one because 0 is not a hero id
hidden_shape = input_shape//2


def get_samples(data, index, max_value, min_value):
    index_of_samples = []
    for i in range(len(data)):
        if data[i][index] > max_value or data[i][index] < min_value:
            continue
        index_of_samples.append(i)

    return index_of_samples


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def sample_accuracy(predictions, labels, index_list):
    accuracy = 0
    for index in index_list:
        accuracy += int(predictions[index] == labels[index])
    return 100*accuracy/len(index_list)


def plot_accuracy(set_x, set_y, volume=[], x_label='x', y_label='y', title='Tile'):
    plt.plot(set_x, set_y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

    if volume:
        plt.plot(set_x, volume)
        plt.xlabel(x_label)
        plt.ylabel('Volume')
        plt.title(x_label + ' volume (number of matches)')
        plt.show()


if __name__ == '__main__':
    print('Starting')
    t = time.time()
    net_name = input('Enter name of network:')
    net = models.load_model(net_name)
    print('Loaded neural network:', time.time() - t)
    t = time.time()

    eval_samples, eval_labels, match_ids = train_network.create_training_data(190000 * 2, file='evaluation.csv')
    print('Generating evaluation data:', time.time() - t)
    t = time.time()

    raw_prediction = predict_with_model(net, eval_samples)
    flat_raw_predictions = [prediction[0] for prediction in raw_prediction]
    flat_predictions = [1 if prediction > 0.5 else 0 for prediction in flat_raw_predictions]
    accurate_predictions = [int(eval_labels[i] == flat_predictions[i]) for i in range(len(eval_labels))]
    print('Make predictions:', time.time() - t)
    t = time.time()

    print('Predictions:', flat_predictions[:50])
    print('Labels:\t\t', eval_labels[:50])
    print('accuracy:\t', accurate_predictions[:50])
    print('Accurate predictions:', sum(accurate_predictions))
    print('Inaccurate predictions:', len(eval_labels) - sum(accurate_predictions))
    print('Total predictions:', len(eval_labels))
    print('Percentage:', sum(accurate_predictions) / len(eval_labels) * 100)

    x_set = []
    y_set = []
    volume = []
    format_predictions = [[abs(prediction - 0.5)] for prediction in flat_raw_predictions]

    for i in range(1, 70):
        match_id = get_samples(format_predictions, 0, max_value=(i + 0.5) / 100, min_value=(i - 0.5) / 100)
        if len(match_id) < 10:
            continue

        y_set.append(sample_accuracy(flat_predictions, eval_labels, match_id))
        x_set.append(i / 100)
        volume.append(len(match_id))

    print('Plot predictions accuracy 2', time.time() - t)
    plot_accuracy(x_set, y_set, volume, 'Absolute prediction deviation from 0.5', 'Model accuracy (%)',
                  'Model accuracy in relation to model prediction deviation from expected value')
    t = time.time()

    x_set = []
    y_set = []
    volume = []
    format_predictions = [[prediction] for prediction in flat_raw_predictions]
    for i in range(1, 100, 2):
        match_id = get_samples(format_predictions, 0, max_value=(i+1)/100, min_value=(i-1)/100)
        if len(match_id) == 0:
            continue

        y_set.append(sample_accuracy(flat_predictions, eval_labels, match_id))
        x_set.append(i/100)
        volume.append(len(match_id))

    print('Plot predictions accuracy', time.time() - t)
    plot_accuracy(x_set, y_set, volume, 'Prediction value', 'Model accuracy (%)',
                  'Model accuracy in relation to model prediction')
    t = time.time()

    x_set = []
    y_set = []
    volume = []
    for i in range(23, 80, 1):
        match_id = get_samples(eval_samples, 115, max_value=(i+5)*60, min_value=(i-5)*60)
        if len(match_id) == 0:
            continue

        y_set.append(sample_accuracy(flat_predictions, eval_labels, match_id))
        x_set.append(i)
        volume.append(len(match_id))
    print('Plot time', time.time() - t)
    plot_accuracy(x_set, y_set, volume, 'Match duration (minutes)', 'Model accuracy (%)',
                  'Model accuracy in relation to match duration')
    t = time.time()

    x_set = []
    y_set = []
    volume = []
    for i in range(16, 100, 1):
        match_id = get_samples(eval_samples, 116, max_value=i, min_value=i)
        if len(match_id) == 0:
            continue

        y_set.append(sample_accuracy(flat_predictions, eval_labels, match_id))
        x_set.append(i)
        volume.append(len(match_id))

    print('Plot rank', time.time() - t)
    plot_accuracy(x_set, y_set, volume, 'Average team rank', 'Model accuracy (%)',
                  'Model accuracy in relation to match rank')
    t = time.time()
