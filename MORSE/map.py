class Map:

  def __init__(self):

    self.map = None

  def loadMap(self, name):
    np.loadtxt(open("pruebaAgua.csv", "rb"), delimiter=",", skiprows=0)

  def mapToImage(self):
    rescaled = (255.0 / arr.max() * (arr - arr.min())).astype(np.uint8) # (RGB)
    io.imsave('tmp.tif', rescaled)


  def imageCallback(self,data):


  def run(self):
    


def main(args):

  ic = ControllerNode()
  rospy.init_node('ControllerNode', anonymous=True)
  ic.run()


if __name__ == '__main__':
    main(sys.argv)
