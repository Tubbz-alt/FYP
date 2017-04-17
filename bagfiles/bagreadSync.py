import rosbag
import cv2
import sys
from cv_bridge import CvBridge, CvBridgeError

bag = rosbag.Bag('test.bag')
f = open('data.txt','w')
i = 0

for topic, msg, t in bag.read_messages(topics=['/ardrone/front/image_raw', '/joy']):
    f.write("{} {}\n".format(t, msg))
    i += 1
bag.close()
print("total {}".format(i))
