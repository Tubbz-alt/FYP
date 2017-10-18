# Created by: Miguel Sancho

from __future__ import print_function
from pymorse import Morse
import PIL.Image, PIL.ImageOps
import numpy as np
from keras import backend as K
from keras.models import load_model
import sys
import cv2
import base64
import math


class ControllerNode:

    def __init__(self):
        self.model = load_model("forest.h5")
        self.img_rows = 224
        self.img_cols = 224
        self.pitchFactor = -0.077
      
    def imageCallback(self,camera):
        width = camera['width'] # 256 default
        height = camera['height'] # 256 default
        buff = base64.b64decode(camera['image'])  # RGBA base64 encoded

        image = np.ndarray(shape=(height, width, 4), buffer=buff, dtype='uint8')
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        image = cv2.resize(image, (self.img_rows, self.img_cols))
        
        cv2.imshow("Quadrotor view", image)

        return image

    def startQuadrotor(self, quadVel):
        vel = { "v": 2, "w": 0 }
        quadVel.publish(vel)

    def predict(self, data):
        image = np.array(data).reshape(1, self.img_rows, self.img_cols, 3)
        prediction = self.model.predict(image)
        deg = prediction.argmax(1)[0] * 20
        rads = self.toRads(deg)

        return { "yaw": rads, "pitch": self.pitchFactor, "roll": 0 }

    def toRads(self, direction):
        if direction < 180:
            direction = -(math.radians(direction))
        else: 
            direction = math.radians(360 - direction)

        return direction


    def run(self):
        with Morse() as morse:
            morse.deactivate('quadrotor.teleport')
            quadVel = morse.quadrotor.motion
            quadDir = morse.quadrotor.orientation
            
            self.startQuadrotor(quadVel)

            while True:
                camera = morse.quadrotor.camera.get()
                image = self.imageCallback(camera)
                orientation = self.predict(image)
                print(orientation)

                quadDir.publish(orientation)
                
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

        cv2.destroyAllWindows()


def main(args):

  node = ControllerNode()
  node.run()


if __name__ == '__main__':
    main(sys.argv)