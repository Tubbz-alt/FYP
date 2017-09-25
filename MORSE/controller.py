from pymorse import Morse

i = 0
with Morse() as morse:
    while i < 1:
        #quadVel = morse.quadrotor.motion.set_speed(3, 0)
        quadVel = morse.quadrotor.motion

        waypoint = {    "v": 1, \
                                "w": 0, \

                            }
        #print(vel)
        quadVel.publish(waypoint)
        i = i +1
