# Created by: Miguel Sancho

import sys
import numpy as np
import math
from scipy.misc import imresize, imsave

class Map:

    def __init__(self, name):
        self.map = np.loadtxt(open(name, "rb"), delimiter=",", skiprows=0)
        self.height = self.map.shape[0]
        self.width = self.map.shape[1]

    def loadMap(self, name):
        self.map = np.loadtxt(open(name, "rb"), delimiter=",", skiprows=0)
        self.height = self.map.shape[0]
        self.width = self.map.shape[1]

    def toImage(self):
        rescaled = (255.0 / self.map.max() * (self.map - self.map.min())).astype(np.uint8) # (RGB)
        resized = imresize(rescaled, [1000, 1000])
        imsave('tmp.tif', resized)

    def getPoint(self, x, y):
        if x < 0:
          x = int(self.height/2) + abs(x)
        else:
          x = int(self.height/2) - x

        if y < 0:
          y = int(self.width/2) + abs(y)
        else:
          y = int(self.width/2) - y  

        return self.map[x-1][y-1]

    def getDirection(self, x, y):
        direction = self.getPoint(x, y)
        toNp = int(direction/20)

        if direction < 180:
            rads = -(math.radians(direction))
        else: 
            rads = math.radians(360 - direction)

        return {"rads": rads, "deg": direction, "dir": toNp}


def main(args):
  map = Map("maps/forest.csv")
  #map.loadMap("maps/plane.csv")
  map.toImage()

  print(map.getPoint(0,8))



if __name__ == '__main__':
    main(sys.argv)
