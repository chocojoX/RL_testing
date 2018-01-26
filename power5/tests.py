import numpy as np
import copy
import time
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.optimizers import SGD, Adadelta, Adam


def load_data():
    X = np.load("data/X.pkl.npy")
    Y = np.load("data/Y.pkl.npy")
    return X, Y


def build_model(size):
    input_shape = (size, size, 1)
    model = Sequential()
    model.add(Conv2D(20, (5, 5), padding='same', activation='relu', input_shape=input_shape))
    # model.add(Dropout(0.25))

    # model.add(Conv2D(16, (4, 4), kernel_initializer='random_uniform', padding='same', activation='sigmoid'))
    # # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(12, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mse', optimizer='adam')
    return model



if __name__=="__main__":
    X, Y = load_data()
    size = X[0].shape[0]
    print("shape : %i"%size)
    print(X.shape, Y.shape)
    model = build_model(size)
    model.fit(X, Y, epochs=30, batch_size=120)
    pass
