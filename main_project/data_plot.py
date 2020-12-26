import matplotlib.pyplot as plt


def generate_plot_data(data_set, data_labels, data_predictions, index, index_value):
    x_set = []
    y_set = []
    for value in index_value:
        adjusted_match_set = []
        accuracy = 0
        data_amount = 0
        for data_index in range(len(data_set)):
            if data_set[data_index][index] != value:
                continue
            data_amount += 1
            accuracy += data_labels[data_index] == data_predictions[data_index]

        if data_amount != 0:
            x_set.append(value)
            y_set.append(accuracy/data_amount)

    return x_set, y_set


def duration_data(data_set, data_labels, data_predictions, index, index_value):
    x_set = []
    y_set = []
    for value in index_value:
        adjusted_match_set = []
        accuracy = 0
        data_amount = 0
        for data_index in range(len(data_set)):
            if data_set[data_index][index]//60 != value:
                continue
            data_amount += 1
            accuracy += data_labels[data_index] == data_predictions[data_index]

        if data_amount != 0:
            x_set.append(value)
            y_set.append(accuracy/data_amount)

    return x_set, y_set


def plot_accuracy(set_x, set_y, x_label='x', y_label='y'):
    plt.plot(set_x, set_y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


