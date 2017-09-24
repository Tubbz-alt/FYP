#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <forest> environment

Feel free to edit this template as you like!
"""

from morse.builder import *


quadrotor = Quadrotor()


quadrotor.translate(3.0, 0.0, -4.0)
quadrotor.rotate(0.0, 0.0, 1.57)

motion = MotionVW()
quadrotor.append(motion)


keyboard = Keyboard()
quadrotor.append(keyboard)
keyboard.properties(ControlType = 'Position')

pose = Pose()
# place your component at the correct location
pose.translate(3.0, 0.0, -4.0)
pose.rotate(0.0, 0.0, 1.57)

quadrotor.append(pose)

camera = VideoCamera()

camera.translate(3.0, 0.0, -4.0)
camera.rotate(0.0, 0.0, 1.57)
quadrotor.append(camera)
# camera.properties(cam_far=800)
camera.add_stream('socket')  # for external Python script
pose.add_interface('socket')
quadrotor.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('models/plane.blend', fastmode = False)
env.set_camera_location([-18.0, -6.7, 19.8])
env.set_camera_rotation([1.09, 0, -1.14])

