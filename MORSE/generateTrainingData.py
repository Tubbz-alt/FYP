# Created by: Miguel Sancho

import mathutils
import base64
import numpy
import cv2

from map import *
from math import pi
from pymorse import Morse
from random import randint

def checkLimit(x, y):
    if x > 30:
        return True
    else:
        return False

def teleport(quadTele):
    x = randint(-43, 32)
    y = randint(-48, 46)

    morse.deactivate('quadrotor.motion')
    morse.activate('quadrotor.teleport')

    destination = { "x": x, \
                    "y": y, \
                    "z": 15, \
                    "yaw": 0, \
                    "pitch": 0, \
                    "roll": 0, \
                   }
    quadTele.publish(destination)
    
    morse.deactivate('quadrotor.teleport')
    morse.activate('quadrotor.motion')
    
    

i = 0
f = open('trainingData/data.txt','w')

map = Map()
map.loadMap("maps/pruebaAgua.csv")

with Morse() as morse:
    morse.deactivate('quadrotor.teleport')
    quadTele = morse.quadrotor.teleport
    quadVel = morse.quadrotor.motion
    quadDir = morse.quadrotor.orientation

    vel = { "v": 2, \
            "w": 0, \
          }
    
    quadVel.publish(vel)
    
    while True:
        camera = morse.quadrotor.camera.get()
        quadPose = morse.quadrotor.pose.get()
        x = quadPose['x']
        y = quadPose['y']

        direction = map.getDirection(round(x), round(y))
        print("Location X,Y :({} , {}) Direction: {}".format(x, y, direction))

        orientation = { "yaw": direction['rads'], \
                        "pitch": 0, \
                        "roll": 0, \
                      }
        quadDir.publish(orientation)

        width = camera['width'] # 256 default
        height = camera['height'] # 256 default
        buff = base64.b64decode(camera['image'])  # RGBA base64 encoded

        image = numpy.ndarray(shape=(height, width, 4), buffer=buff, dtype='uint8')
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        # image = cv2.resize(image, (512, 512))
        cv2.imshow("Robot view", image)

        fileName = 'trainingData/'+str(i)+'.jpg'
        cv2.imwrite(fileName, image)
        f.write(fileName + ' ' + str(direction['dir']) + '\n')

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        
        if checkLimit(x, y):
            teleport(quadTele)

        i = i + 1
cv2.destroyAllWindows()

