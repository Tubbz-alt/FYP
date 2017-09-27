# Created by: Miguel Sancho

import base64
import numpy
import cv2

from pymorse import Morse
from map import *
from math import pi

i = 0
f = open('data.txt','w')

map = Map()
map.loadMap("maps/pruebaAgua.csv")

with Morse() as morse:
    quadVel = morse.quadrotor.motion
    quadDir = morse.quadrotor.orientation

    vel = { "v": 1, \
            "w": 0, \
          }
    
    quadVel.publish(vel)
    
    while True:
        camera = morse.quadrotor.camera.get()
        quadPose = morse.quadrotor.pose.get()
        direction = map.getDirection(round(quadPose['x']), round(quadPose['y']))
        print("Location X,Y :({} , {}) Direction: {}".format(quadPose['x'], quadPose['y'], direction))

        orientation = { "yaw": direction['rads'], \
                        "pitch": 0, \
                        "roll": 0, \
                      }
        quadDir.publish(orientation)

        width = camera['width']
        height = camera['height']
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
        i = i + 1
cv2.destroyAllWindows()

