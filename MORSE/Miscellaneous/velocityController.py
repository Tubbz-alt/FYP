# Created by: Miguel Sancho

from pymorse import Morse

i = 0
with Morse() as morse:
    while i < 1:
        quadVel = morse.quadrotor.velocity

        vel = {   "vx": 0, \
                  "vy": 1, \
                  "vz": 0, \
                  "vyaw": 0, \
                  "tolerance": 0.2 \
              }
        print(vel)
        quadVel.publish(vel)
        i = i +1
