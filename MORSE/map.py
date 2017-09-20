import sys
import numpy as np
from math import pi
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
      x = 82 - abs(x)
    else:
      x = 82 + x

    if y < 0:
      y = 81 + abs(y)
    else:
      y = 81 - y  

    return self.map[y][x]



def main(args):
  map = Map()
  map.loadMap("maps/pruebaAgua.csv")
  map.toImage()
  print(map.getPoint(2,73))


if __name__ == '__main__':
    main(sys.argv)
