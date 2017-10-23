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
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
import matplotlib.pyplot as plt

from dataManager import *
from resnet50 import *


batch_size = 30
classes = 5
nb_epoch = 50
dataManager = dataManager()
dataManager.newDataSet()

X_train, Y_train, X_test, Y_test, input_shape = dataManager.getTrainingData()

print(X_train.shape, 'train samples')
print(X_test.shape, 'test samples')
print(input_shape,'input_shape')
print(nb_epoch,'epochs')

model = ResNet50(include_top=True, weights=None,
             input_tensor=None, input_shape=None,
             pooling=None,
             classes=18)

#optimizer = SGD(lr = 0.01,momentum=0.1,nesterov = False)
filepath = "weights-improvement-{epoch:02d}-{val_acc:.2f}.h5"

early_stopping = EarlyStopping(monitor='loss', patience=2)
model_checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)

model.compile(loss = 'categorical_crossentropy',optimizer = 'adam', metrics = ['accuracy'])

history = model.fit(X_train, Y_train, batch_size = batch_size, epochs = nb_epoch,
	verbose = 1, validation_data = (X_test, Y_test), callbacks=[early_stopping, model_checkpoint])
score = model.evaluate(X_test, Y_test, verbose = 1)

# file name to save model
filename = 'plane.h5'

# save network model
model.save(filename)

# load neetwork model
#model = load_model(filename)