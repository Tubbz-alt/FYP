# Created by: Miguel Sancho

from pymorse import Morse
from map import *
from math import pi

map = Map()
map.loadMap("maps/pruebaAgua.csv")

with Morse() as morse:
    quadVel = morse.quadrotor.motion
    quadDir = morse.quadrotor.orientation

    vel = { "v": 3, \
            "w": 0, \
          }
    
    quadVel.publish(vel)
    
    while True:
        quadPose = morse.quadrotor.pose.get()
        print("X: {}".format(quadPose['x']))
        print("Y: {}".format(quadPose['y']))
        direction = map.getDirection(round(quadPose['x']), round(quadPose['y']))
        print("Direction: {}".format(direction))
        orientation = { "yaw": direction, \
                        "pitch": 0, \
                        "roll": 0, \
        }
        quadDir.publish(orientation)

