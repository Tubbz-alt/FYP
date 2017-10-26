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
        self.saveDirection = False
        self.normalize = False
        self.saveToDisk = False
        self.poseHasChanged = False
        self.lastDirection = 0
        self.lastNpDir = 0
        self.lastPose = 0
        self.pitchFactor = -0.077
        self.normFactor = 10
        self.map = Map("maps/forest.csv")
        self.lapCounter = 0
        self.dataCounter = 0

    def startQuadrotor(self, morse):
        quadVel = morse.quadrotor.motion
        quadPose = morse.quadrotor.pose.get()

        self.lastDirection = self.map.getDirection(round(quadPose['x']), round(quadPose['y']))['deg']
        vel = { "v": 2, "w": 0 }

        quadVel.publish(vel)

    def checkLimit(self, x, y):
        if x > 60:
            return True
        else:
            return False

    def checkNormalization(self):
        if self.lapCounter > self.normFactor:
            self.normalize = True

    def teleport(self, quadTele, morse):
        x = randint(-65, -45)
        y = randint(-51, 51)
        #x = randint(-56, -53)
        #y = randint(-51, -46)

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
        #print("Location X,Y :({} , {}) Direction: {}".format(x, y, direction))

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

    def poseChanged(self, quadPose):
        newPose = round(quadPose['yaw'], 5)

        if (abs(self.lastPose-newPose) > 0.00000):

            self.poseHasChanged = True
            self.lastPose = newPose
            return True
        else:
            self.poseHasChanged = False
            return False
            
    def dirToNp(self, newDir):
        if newDir > 0:
            if newDir > 20:
                toNp = 4
            else:
                toNp = 3
        elif newDir < 0:
            if newDir < -20:
                toNp = 1
            else:
                toNp = 2
        else:
            toNp = self.lastNpDir

        self.lastNpDir = toNp

        return toNp

    def getTurningDir(self, direction, quadPose):
        newDir =  (self.lastDirection - direction['deg'])
        if abs(newDir) < 180:
            newDir = -newDir
        toNp = 0

        if (self.poseChanged(quadPose)):
            self.lastDirection = direction['deg']
            toNp = self.dirToNp(newDir)
        self.lastNpDir = toNp

        return toNp

    def save(self, image, direction, pose):
        if self.saveDirection:
            self.checkSave(image, direction['dir'])
        else:
            self.checkSave(image, self.getTurningDir(direction, pose))


    def checkSave(self, image, direction):
        if self.normalize:
            if self.poseHasChanged:
               self.writeFile(image, direction) 
        else:
            self.writeFile(image, direction)


    def plot(self, x, y):
        if self.dataCounter % 2 == 0:
            self.f.write(str(int(x)) + ' ' + str(int(y)) + '\n')
   
    def run(self):
        self.f = open('pathPlots.txt','a')
        
        with Morse() as morse:
            morse.deactivate('quadrotor.teleport')
            quadTele = morse.quadrotor.teleport
            quadDir = morse.quadrotor.orientation
            
            self.startQuadrotor(morse)

            while True:
                print("Iteration: " + str(self.dataCounter) + " Lap: " + str(self.lapCounter))
                camera = morse.quadrotor.camera.get()
                quadPose = morse.quadrotor.pose.get()
                x = quadPose['x']
                y = quadPose['y']

                direction = self.map.getDirection(round(x), round(y))
                orientation = self.getOrientation(x, y, direction)
                quadDir.publish(orientation)

                image = self.imageCallback(camera)

                if self.saveToDisk:
                    self.save(image, direction, quadPose)

                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
                
                if self.checkLimit(x, y):
                    self.teleport(quadTele, morse)
                    self.checkNormalization()
                self.plot(x, y)

                self.dataCounter = self.dataCounter + 1

        cv2.destroyAllWindows()

def main(args):

  node = DataNode()
  node.run()


if __name__ == '__main__':
    main(sys.argv)
