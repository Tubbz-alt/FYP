from __future__ import print_function
from PIL import Image, ImageOps
import numpy as np
import glob

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD, adam, adadelta
from keras.models import load_model
from keras.callbacks import EarlyStopping
from keras import backend as K
import matplotlib.pyplot as plt

from dataManager import *


batch_size = 30
nb_classes = 8
nb_epoch = 30
dataManager = dataManager()
dataManager.newDataSet()

img_rows, img_cols = 256, 256

X_train, Y_train, X_test, Y_test, input_shape = dataManager.getTrainingData()

print(X_train.shape, 'train samples')
print(X_test.shape, 'test samples')
print(input_shape,'input_shape')
print(nb_epoch,'epochs')

#
# Neural Network Structure
#
def create_model():
	model = Sequential()
	# first set of CONV => RELU => POOL
	model.add(Convolution2D(20, 5, 5, border_mode="same",
	input_shape=(input_shape)))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

	# second set of CONV => RELU => POOL
	model.add(Convolution2D(50, 5, 5, border_mode="same"))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	model.add(Dropout(0.5)) # reducing overfitting

	# set of FC => RELU layers
	model.add(Flatten())
	model.add(Dense(500))
	model.add(Activation("relu"))

	# softmax classifier
	model.add(Dense(nb_classes))
	model.add(Activation("softmax"))
	##model.summary()

	return model


optimizer = SGD(lr = 0.01,momentum=0.1,nesterov = False)
early_stopping = EarlyStopping(monitor='loss', patience=3)
#model = load_model('homus_cnn.h5')
model = create_model()
model.compile(loss = 'categorical_crossentropy',optimizer = optimizer, metrics = ['accuracy'])

history = model.fit(X_train, Y_train, batch_size = batch_size, nb_epoch = nb_epoch,
	verbose = 2, validation_data = (X_test, Y_test), callbacks=[early_stopping])
score = model.evaluate(X_test, Y_test, verbose = 1)

#
# Results
#

print('Test score:', score[0])
print('Test accuracy:', score[1])

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# file name to save model
filename = 'plane.h5'

# save network model
model.save(filename)

# load neetwork model
#model = load_model(filename)