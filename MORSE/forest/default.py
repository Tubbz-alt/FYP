#! /usr/bin/env morseexec
# Created by: Miguel Sancho

from morse.builder import *
from math import inf


quadrotor = Quadrotor()

quadrotor.translate(-54, -51, 7)
#quadrotor.rotate(0.0, 0.0, pi/2)

######## KEYBOARD ########

#keyboard = Keyboard()

#quadrotor.append(keyboard)
#keyboard.properties(ControlType = 'Position')

######## CAMERA ########

camera = VideoCamera() # H & W = 256

camera.translate(0.32, 0.0, 0.0)
camera.properties(cam_far=1000, cam_focal=15.0)
quadrotor.append(camera)
camera.add_interface('socket')

######## POSE ########

pose = Pose()

quadrotor.append(pose)
pose.add_interface('socket')

######## MOTION HANDLER ########

motion = MotionVW()

quadrotor.append(motion)
motion.add_interface('socket')

######## ORIENTATION HANDLER ########

orientation = Orientation()

orientation.properties(speed=0.5, tolerance=0.02, ControlType='Position')
quadrotor.append(orientation)
orientation.add_interface('socket')

######## TELEPORT HANDLE ########

teleport = Teleport()

quadrotor.append(teleport)
teleport.add_interface('socket')

######## ENVIRONMENT ########

# set 'fastmode' to True to switch to wireframe mode
env = Environment('models/path.blend', fastmode=False)
env.set_camera_location([-70, -60.0, 19.8])
env.set_camera_rotation([1.09, 0, -1.14])

