# Created by: Miguel Sancho

from pymorse import Morse
from math import pi

with Morse() as morse:
    morse.deactivate('quadrotor.motion')
    #morse.activate('robot.teleport')
    quadVel = morse.quadrotor.teleport

    waypoint = {    "x": 0, \
                    "y": 0, \
                    "z": 10, \
                    "yaw": 0, \
                    "tolerance": 0.5 \
                }
    
    quadVel.publish(waypoint)
    
    while True:
        None

