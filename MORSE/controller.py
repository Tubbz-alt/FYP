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
        self.forestModel = load_model("forest.h5")
        self.behaviourModel = load_model("behaviour.h5")
        self.img_rows = 224
        self.img_cols = 224
        self.pitchFactor = -0.077
        self.useOrientation = False
        self.lastBehaviour = 0
        self.iteration = 0
      
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

    def predictBehaviour(self, image):
        behaviour = self.behaviourModel.predict(image).argmax(1)[0]
        self.lastBehaviour = behaviour

        if behaviour < 1:
            print("FOREST")
        else:
            print("PATH")

        return behaviour

    def predictAction(self, behaviour, image):
        if behaviour < 1:
            action = self.forestModel.predict(image)
        else:
            None

        return action

    def predict(self, data):
        image = np.array(data).reshape(1, self.img_rows, self.img_cols, 3)

        if self.iteration % 5 == 0:
            behaviour = self.predictBehaviour(image)
        else: 
            behaviour = self.lastBehaviour

        action = self.predictAction(behaviour, image)
        rads = self.toRads(action)

        if self.useOrientation:
            prediction = { "yaw": rads, "pitch": self.pitchFactor, "roll": 0 }
        else:
            prediction = { "v": 2, "w": rads }
            
        return prediction

    def getTurningDirection(self, pred):
        if pred < 1:
            direction = 0
            print("Going Straight")
        elif pred < 3:
            direction = -(math.radians((pred * 20)))
            print("Turning Left " + str(direction) + "rads")
        else:
            direction = (math.radians((pred - 2) * 20))
            print("Turning Right " + str(direction) + "rads")

        return direction

    def getOrientation(self, pred):
        direction = pred * 20

        if direction < 180:
            direction = -(math.radians(direction))
        else: 
            direction = math.radians(360 - direction)

        return direction

    def toRads(self, prediction):
        pred = prediction.argmax(1)[0]
        
        if self.useOrientation:
            direction = self.getOrientation(pred) # using full 360 degrees
        else:
            direction = self.getTurningDirection(pred) # using left/right turns

        return direction

    def stabilizeAltitude(self, morse, quadDir):
        quadPose = morse.quadrotor.pose.get()

        quadDir.publish({ "yaw": quadPose['yaw'], "pitch": self.pitchFactor, "roll": 0 })

    
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
                
                if self.useOrientation:
                    quadDir.publish(orientation)
                else:
                    quadVel.publish(orientation)
                    self.stabilizeAltitude(morse, quadDir)
                    

                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

                if self.checkLimit(quadPose['x'], quadPose['y']):
                    self.teleport(quadTele, morse)

                self.iteration += 1

        cv2.destroyAllWindows()


def main(args):

  node = ControllerNode()
  node.run()


if __name__ == '__main__':
    main(sys.argv)