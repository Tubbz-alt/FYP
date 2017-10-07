# Created by: Miguel Sancho

import sys
import numpy as np
import math
from skimage import io, util

class Map:

    def __init__(self):
        self.map = None

    def loadMap(self, name):
        self.map = np.loadtxt(open(name, "rb"), delimiter=",", skiprows=0)

    def toImage(self):
        rescaled = (255.0 / self.map.max() * (self.map - self.map.min())).astype(np.uint8) # (RGB)
        io.imsave('tmp.tif', rescaled)

    def getPoint(self, x, y):
        if x < 0:
          x = 81 + abs(x)
        else:
          x = 81 - x

        if y < 0:
          y = 80 + abs(y)
        else:
          y = 80 - y  

        return self.map[x][y]

    def getDirection(self, x, y):
        direction = self.getPoint(x, y)
        toNp = int(direction/45)

        if direction < 180:
            direction = -(math.radians(direction))
        else: 
            direction = math.radians(360 - direction)

        return {"rads": direction, "dir": toNp}



def main(args):
  map = Map()
  map.loadMap("maps/pruebaAgua.csv")
  map.toImage()
  print(map.getPoint(-3,75))
  print(map.getDirection(-3,75))
  print(map.getPoint(80,2))  
  print(map.getDirection(27,80))



if __name__ == '__main__':
    main(sys.argv)
