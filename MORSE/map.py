# Created by: Miguel Sancho

import sys
import numpy as np
import math
from skimage import io, util

class Map:

    def __init__(self):
        self.map = None
        self.width = None
        self.height = None

    def loadMap(self, name):
        self.map = np.loadtxt(open(name, "rb"), delimiter=",", skiprows=0)
        self.height = self.map.shape[0]
        self.width = self.map.shape[1]

    def toImage(self):
        rescaled = (255.0 / self.map.max() * (self.map - self.map.min())).astype(np.uint8) # (RGB)
        io.imsave('tmp.tif', rescaled)

    def getPoint(self, x, y):
        if x < 0:
          x = int(self.height/2) + abs(x)
        else:
          x = int(self.height/2) - x

        if y < 0:
          y = int(self.width/2) + abs(y)
        else:
          y = int(self.width/2) - y  

        return self.map[x][y]

    def getDirection(self, x, y):
        direction = self.getPoint(x, y)
        toNp = int(direction/20)

        if direction < 180:
            direction = -(math.radians(direction))
        else: 
            direction = math.radians(360 - direction)

        return {"rads": direction, "dir": toNp}


def main(args):
  map = Map()
  map.loadMap("maps/pruebaAgua.csv")
  #map.toImage()

  print(map.getPoint(-3,75))
  print(map.getDirection(-3,75))
  print(map.getPoint(80,2))  
  print(map.getDirection(27,80))


if __name__ == '__main__':
    main(sys.argv)
