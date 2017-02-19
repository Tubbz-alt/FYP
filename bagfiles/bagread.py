import rosbag
bag = rosbag.Bag('test.bag')
for topic, msg, t in bag.read_messages(topics=['/ardrone/front/image_raw']):
    print msg
bag.close()
