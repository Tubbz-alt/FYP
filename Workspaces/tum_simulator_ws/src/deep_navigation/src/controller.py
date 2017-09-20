#!/usr/bin/env python
from __future__ import print_function
import PIL.Image, PIL.ImageOps
import numpy as np
import roslib
from keras import backend as K
from keras.models import load_model
import time
roslib.load_manifest('deep_navigation')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
import rosgraph
import sys, socket




class ControllerNode:

  def __init__(self):

    self.bridge = CvBridge()
    self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.imageCallback)

    self.lastLinearVelocityX = None
    self.lastAngularVelocityZ = None
    self.lastImage = None
    self.model = load_model("/home/miguel/tum_simulator_ws/src/deep_navigation/src/model.h5")

  def imageCallback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.lastImage = cv_image
    except CvBridgeError as e:
      print(e)


  def run(self):
      i=0
      while not rospy.is_shutdown():
        #rospy.spin()
        #wait for user keyboard iput
        #try:
      	#     cv2.imshow("Image window", self.lastImage)
        #     cv2.waitKey(3)
        #except Exception as e:
        #    print(e)
        r_im = cv2.resize(self.lastImage, (220,180))
        np_im = np.asarray(r_im).reshape(1, 220,180,3)
        output = self.model.predict(np_im)
        print(output)
        move_cmd = Twist()
        #if output[0][0] < 1:
        #    move_cmd.linear.x = output[0][0]
        #else:
        #    move_cmd.linear.x = 1
        move_cmd.linear.x = 0.5
        move_cmd.linear.y = 0
        move_cmd.linear.z = 0
        move_cmd.angular.x = 0
        move_cmd.angular.y = 0
        #move_cmd.angular.z = output[0][1]
        move_cmd.angular.z = output[0]
        self.cmd_vel.publish(move_cmd)
        i+=1

def main(args):

  ic = ControllerNode()
  rospy.init_node('ControllerNode', anonymous=True)
  ic.run()


if __name__ == '__main__':
    main(sys.argv)
