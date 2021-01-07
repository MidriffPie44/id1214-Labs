import matplotlib.pyplot as plt


def generate_plot_data(data_set, data_labels, data_predictions, index, index_value, deviation=0):
    x_set = []
    y_set = []
    volume = []
    for value in index_value:
        accuracy = 0
        data_amount = 0
        for data_index in range(len(data_set)):
            if data_set[data_index][index] < value - deviation or data_set[data_index][index] + deviation > value:
                continue
            data_amount += 1
            accuracy += data_labels[data_index] == data_predictions[data_index]

        if data_amount > 20:
            x_set.append(value)
            y_set.append((accuracy*100)/data_amount)
            volume.append(data_amount)
            
    return x_set, y_set, volume


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


    


