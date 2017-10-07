# Created by: Miguel Sancho

import cv2
import sys
import numpy as np
from PIL import Image
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

class dataManager:
    X = None
    Y = None
    img_rows = 224
    img_cols = 224

    def newDataSet(self):
        image_list = []
        output_list = []
        f = open('trainingData/data.txt', 'r')
        for line in f:
            dataLine = line.split(' ', 2)
            #im = Image.open(dataLine[0])
            #im = Image.open(dataLine[0]).resize((img_rows,img_cols)) # resize
            #im = Image.open(dataLine[0]).resize((img_rows,img_cols)).convert('L') # B & W
            image = cv2.imread(dataLine[0])
            image = cv2.resize(image, (self.img_rows, self.img_cols))
            outputs = [dataLine[1]]
            image_list.append(np.array(image))
            output_list.append(np.array(outputs))

        n = len(image_list)	# Total examples
        print("total images: {}".format(n))

        self.X = np.asarray(image_list).reshape(n,self.img_rows,self.img_cols,3)
        self.Y = np_utils.to_categorical(np.asarray(output_list), 8)

        print(self.X.shape)
        print(self.Y.shape)
        
    def saveDataSet(self):
        None
    def loadDataSet(self):
        None
    def getTrainingData(self, testSize = 0.1, randomState = 23):
        input_shape = (self.img_rows, self.img_cols, 3)

        X_train, X_test, Y_train, Y_test = train_test_split(
        self.X, self.Y, test_size=testSize, random_state=randomState)

        return X_train, Y_train, X_test, Y_test, input_shape


def main(args):
    manager = dataManager()
    manager.newDataSet()


if __name__ == '__main__':
    main(sys.argv)
