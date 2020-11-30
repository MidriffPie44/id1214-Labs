import keras.layers as layers
import keras.optimizers as optimizers
from keras import Sequential
import numpy as np
import random


def create_new_seq_model():
    model = Sequential()
    weights = 'random_uniform'

    model.add(layers.Dense(50, input_shape=(1,), activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(50, activation='relu', kernel_initializer=weights))
    model.add(layers.Dense(1, activation='linear', kernel_initializer=weights))

    model.compile(optimizers.Adam(), loss='mse')

    return model


def create_training_data(amount, max_num, func):
    domain = [random.randint(0, max_num) for i in range(amount)]
    results = [func(d) for d in domain]

    return domain, results


def predict_with_model(model, samples):
    return model.predict(np.array(samples))


def train_model(model, samples, labels, epochs, batch_size):
    model.fit(np.array(samples), np.array(labels), epochs=epochs, batch_size=batch_size)


def func(x):
    return x*3+20


if __name__ == '__main__':
    data_samples, data_labels = create_training_data(10000, 1000, func)
    eval_samples, eval_labels = create_training_data(5, 100, func)

    net = create_new_seq_model()

    train_model(net, data_samples, data_labels, 100, 100)

    eval_prediction = predict_with_model(net, eval_samples)

    print('Predictions:', [prediction[0] for prediction in eval_prediction])
    print('Labels:', eval_labels)



