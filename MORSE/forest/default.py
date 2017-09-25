#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <forest> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
from math import pi


quadrotor = Quadrotor()

quadrotor.translate(3.0, 0.0, 15)
quadrotor.rotate(0.0, 0.0, pi/2)

######## KEYBOARD ########

#keyboard = Keyboard()

#quadrotor.append(keyboard)
#keyboard.properties(ControlType = 'Position')

######## CAMERA ########

camera = VideoCamera()

camera.translate(0.32, 0.0, 0.0)
camera.rotate(0.0, 0.0, pi/2)
quadrotor.append(camera)
camera.add_interface('socket')
# camera.properties(cam_far=800)

######## POSE ########

pose = Pose()

#pose.translate(3.0, 0.0, -4.0)
pose.rotate(0.0, 0.0, pi/2)
quadrotor.append(pose)
pose.add_interface('socket')

######## MOTION HANDLER ########

motion = MotionVW()

quadrotor.append(motion)
motion.add_interface('socket')

######## ORIENTATION HANDLER ########

orientation = Orientation()
quadrotor.append(orientation)
orientation.add_interface('socket')

######## ENVIRONMENT ########

# set 'fastmode' to True to switch to wireframe mode
env = Environment('models/plane.blend', fastmode = False)
env.set_camera_location([-18.0, -6.7, 19.8])
env.set_camera_rotation([1.09, 0, -1.14])

