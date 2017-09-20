#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('deep_navigation')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import time
import sys




class NavigationNode:

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.imageCallback)
    self.odom_sub = rospy.Subscriber("/cmd_vel",Twist,self.odomCallback)

    self.linearVelocities = None
    self.angularVelocities = None
    self.lastImage = None

  def odomCallback(self, data):
    self.linearVelocities = data.linear
    self.angularVelocities = data.angular
    #print("Linear:",data.linear.x)
    #self.lastLinearVelocityX = data.twist.twist.linear.x
    #print("Angular",data.twist.twist.angular)
    #self.lastAngularVelocityZ = data.twist.twist.angular.z

  def imageCallback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.lastImage = cv_image
    except CvBridgeError as e:
      print(e)

  def run(self):

    f = open('data.txt','w+')

    i=0
    while not rospy.is_shutdown():
        # Save Velocities and Image
        print("Linear: {}, {}, {}".format(self.linearVelocities.x, self.linearVelocities.y, self.linearVelocities.z))
        print("Angular: {}, {}, {}".format(self.angularVelocities.x, self.angularVelocities.y, self.angularVelocities.z))
        fileName = 'dataset-drone/'+str(i)+'.jpg'
        cv2.imwrite(fileName, self.lastImage)
        f.write(fileName+ ' '+"{} {} {} {} {} {}".format(self.linearVelocities.x, self.linearVelocities.y, self.linearVelocities.z, self.angularVelocities.x, self.angularVelocities.y, self.angularVelocities.z)+'\n')
        i+=1
        time.sleep(0.2)

    print("Shutting down")
    f.close()
    #cv2.destroyAllWindows()


def main(args):
  ic = NavigationNode()
  rospy.init_node('NavigationNode', anonymous=True)
  ic.run()


if __name__ == '__main__':
    main(sys.argv)
