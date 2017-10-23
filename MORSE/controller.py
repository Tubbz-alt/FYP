# Created by: Miguel Sancho

from __future__ import print_function
from pymorse import Morse
import PIL.Image, PIL.ImageOps
import numpy as np
from keras import backend as K
from keras.models import load_model
from random import randint
import sys
import cv2
import base64
import math


class ControllerNode:

    def __init__(self):
        self.model = load_model("path.h5")
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

    def checkLimit(self, x, y):
        if x > 40:
            return True
        else:
            return False    

    def teleport(self, quadTele, morse):
        x = randint(-65, -45)
        y = randint(-51, 51)

        morse.deactivate('quadrotor.motion')
        morse.activate('quadrotor.teleport')

        destination = { "x": x, \
                        "y": y, \
                        "z": 7, \
                        "yaw": 0, \
                        "pitch": 0, \
                        "roll": 0, \
                       }
        quadTele.publish(destination)
        
        morse.deactivate('quadrotor.teleport')
        morse.activate('quadrotor.motion')

    def predict(self, data):
        image = np.array(data).reshape(1, self.img_rows, self.img_cols, 3)
        prediction = self.model.predict(image)
        deg = prediction.argmax(1)[0] * 20
        rads = self.toRads(deg)

        print("direction: " + str(deg))

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
            quadTele = morse.quadrotor.teleport
            quadVel = morse.quadrotor.motion
            quadDir = morse.quadrotor.orientation
            
            self.startQuadrotor(quadVel)

            while True:
                camera = morse.quadrotor.camera.get()
                image = self.imageCallback(camera)
                orientation = self.predict(image)
                quadPose = morse.quadrotor.pose.get()
                x = quadPose['x']
                y = quadPose['y']

                quadDir.publish(orientation)
                
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

                if self.checkLimit(x, y):
                    self.teleport(quadTele, morse)

        cv2.destroyAllWindows()


def main(args):

  node = ControllerNode()
  node.run()


if __name__ == '__main__':
    main(sys.argv)