#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <forest> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
from math import pi


quadrotor = Quadrotor()

quadrotor.translate(3.0, 0.0, 15)
quadrotor.rotate(0.0, 0.0, pi/2)

motion = MotionVW()
quadrotor.append(motion)

######## KEYBOARD ########

keyboard = Keyboard()

quadrotor.append(keyboard)
keyboard.properties(ControlType = 'Position')

######## POSE ########

pose = Pose()

#pose.translate(3.0, 0.0, -4.0)
pose.rotate(0.0, 0.0, pi/2)

quadrotor.append(pose)

######## CAMERA ########

camera = VideoCamera()

camera.translate(0.0, -0.31, 0.0)
camera.rotate(0.0, 0.0, pi/2)

quadrotor.append(camera)
# camera.properties(cam_far=800)

######## ORIENTATION HANDLER ########

# creates a new instance of the actuator
orientation = Orientation()

#orientation.translate(3.0, 0.0, -4.0)
#orientation.rotate(0.0, 0.0, pi/2)

quadrotor.append(orientation)

######## VELOCITY HANDLER ########

velocity = RotorcraftVelocity()

#velocity.translate(3.0, 0.0, -4.0)
velocity.rotate(0.0, 0.0, pi/2)

quadrotor.append(velocity)

######## STREAMS ########

camera.add_stream('socket')
pose.add_interface('socket')
orientation.add_stream('socket')
velocity.add_interface('socket')
quadrotor.add_default_interface('socket')

######## ENVIRONMENT ########

# set 'fastmode' to True to switch to wireframe mode
env = Environment('models/plane.blend', fastmode = False)
env.set_camera_location([-18.0, -6.7, 19.8])
env.set_camera_rotation([1.09, 0, -1.14])

