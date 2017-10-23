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
        self.saveToDisk = True
        self.lastDirection = 0
        self.lastNpDir = 0
        self.lastPose = 0
        self.pitchFactor = -0.077
        self.normFactor = 10
        self.map = Map("maps/path.csv")
        self.lapCounter = 10
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
        x = -54#randint(-65, -45)
        y = -57#randint(-51, 51)

        morse.deactivate('quadrotor.motion')
        morse.activate('quadrotor.teleport')

        destination = { "x": x, \
                        "y": y, \
                        "z": 7, \
                        "yaw": pi/2, \
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
        print("LAST POSE: " + str(round(quadPose['yaw'], 6)) + " NEW POSE: " + str(newPose))
        print("RESTA: " + str(abs(self.lastPose-newPose)))

        if (abs(self.lastPose-newPose) > 0.00000):
            print("POSE CHANGED")
            self.lastPose = newPose
            return True
        else:
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
        print("LAST DIR: " + str(self.lastDirection))
        print("ACTUAL DIR: " + str(direction['deg']))
        print("NEW DIR: " + str(newDir))
        
        toNp = 0

        if (self.poseChanged(quadPose)):
            self.lastDirection = direction['deg']
            toNp = self.dirToNp(newDir)

        print("Direccion: " + str(toNp))
        self.lastNpDir = toNp

        return toNp

    def save(self, image, direction, pose):
        if self.saveDirection:
            self.checkSave(image, direction['dir'])
        else:
            self.checkSave(image, self.getTurningDir(direction, pose))


    def checkSave(self, image, direction):
        if self.normalize:
            if direction != 0:
               self.writeFile(image, direction) 
        else:
            self.writeFile(image, direction)


    def writeFile(self, image, direction):
        fileName = 'trainingData/' + str(self.dataCounter) + '.jpg'
        cv2.imwrite(fileName, image)
        self.f.write(fileName + ' ' + str(direction) + '\n')
   
    def run(self):
        if self.saveToDisk:
            self.f = open('trainingData/data.txt','a')
        
        with Morse() as morse:
            morse.deactivate('quadrotor.teleport')
            quadTele = morse.quadrotor.teleport
            quadDir = morse.quadrotor.orientation
            
            self.startQuadrotor(morse)

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
                    self.save(image, direction, quadPose)

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
