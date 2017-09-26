# Created by: Miguel Sancho

import base64
import numpy
import cv2
import scipy.misc

from pymorse    import Morse
from scipy.misc import imsave

while True:
  with Morse() as sim:
    data = sim.quadrotor.camera.get()

  width = data['width']
  height = data['height']
  buff = base64.b64decode(data['image'])  # RGBA base64 encoded

  image = numpy.ndarray(shape=(height, width, 4), buffer=buff, dtype='uint8')
  image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
# image = cv2.resize(image, (512, 512))
  cv2.imshow("Robot view", image)
# scipy.misc.imsave('image.jpg', image)

  if cv2.waitKey(1) & 0xff == ord('q'):
    break

cv2.destroyAllWindows()