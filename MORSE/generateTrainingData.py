# Created by: Miguel Sancho

import mathutils
import base64
import numpy
import cv2

from map import *
from math import pi
from pymorse import Morse
from random import randint

class DataNode:

    def __init__(self):
        self.normalize = False
        self.saveToDisk = True
        self.pitchFactor = -0.077
        self.normFactor = 10
        self.map = Map("maps/forest.csv")
        self.lapCounter = 0
        self.dataCounter = 0

    def startQuadrotor(self, quadVel):
        vel = { "v": 2, \
                "w": 0, \
              }
        quadVel.publish(vel)

    def checkLimit(self, x, y):
        if x > 40:
            return True
        else:
            return False

    def checkNormalization(self):
        if self.lapCounter > self.normFactor:
            self.normalize = True

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

        self.lapCounter = self.lapCounter + 1

    def getOrientation(self, x, y, direction):
        print("Location X,Y :({} , {}) Direction: {}".format(x, y, direction))

        return { "yaw": direction['rads'], "pitch": self.pitchFactor, "roll": 0.0 }

    def imageCallback(self, camera):
        width = camera['width'] # 256 default
        height = camera['height'] # 256 default
        buff = base64.b64decode(camera['image'])  # RGBA base64 encoded

        image = numpy.ndarray(shape=(height, width, 4), buffer=buff, dtype='uint8')
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        # image = cv2.resize(image, (512, 512))
        cv2.imshow("Quadrotor view", image)

        return image     

    def save(self, image, direction):
        if self.normalize:
            if direction != 0:
                fileName = 'trainingData/' + str(self.dataCounter) + '.jpg'
                cv2.imwrite(fileName, image)
                self.f.write(fileName + ' ' + str(direction) + '\n')
        else:
            fileName = 'trainingData/' + str(self.dataCounter) + '.jpg'
            cv2.imwrite(fileName, image)
            self.f.write(fileName + ' ' + str(direction) + '\n')
           
    def run(self):
        if self.saveToDisk:
            self.f = open('trainingData/data.txt','w')
        
        with Morse() as morse:
            morse.deactivate('quadrotor.teleport')
            quadTele = morse.quadrotor.teleport
            quadVel = morse.quadrotor.motion
            quadDir = morse.quadrotor.orientation
            
            self.startQuadrotor(quadVel)

            while True:
                camera = morse.quadrotor.camera.get()
                quadPose = morse.quadrotor.pose.get()
                x = quadPose['x']
                y = quadPose['y']

                direction = self.map.getDirection(round(x), round(y))
                orientation = self.getOrientation(x, y, direction)
                quadDir.publish(orientation)

                image = self.imageCallback(camera)

                if self.saveToDisk:
                    self.save(image, direction['dir'])

                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
                
                if self.checkLimit(x, y):
                    self.teleport(quadTele, morse)
                    self.checkNormalization()

                self.dataCounter = self.dataCounter + 1

        cv2.destroyAllWindows()

def main(args):

  node = DataNode()
  node.run()


if __name__ == '__main__':
    main(sys.argv)
