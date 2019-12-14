# Program to cause the Bebop2 to take off, detect follow green PostIt Notes, and land upon recognizing pink PostIt Notes.

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import cv2 # To install: pip3 install opencv-contrib-python
import cv_bridge # To install: sudo apt-get install ros-melodic-cv-bridge
import dlib # To install: pip3 install dlib
import time
from path_planner import *
from analyze_image import *
DISPLAY_IMAGE = True


FLIGHT_TIME = 140 # seconds
FACE_REC_INTERVAL = .8 # seconds
PATH_PLAN_INTERVAL = .5
FRAME_WIDTH = 428
FRAME_HEIGHT = 240

bridge = None
face_detector = dlib.get_frontal_face_detector()
win = dlib.image_window()
last_image = None

drone_pub = None
landing_pub = None

last_img_call = 0

def img_callback(img_msg):
  global bridge, last_image, last_img_call, FACE_REC_INTERVAL, FRAME_WIDTH, FRAME_HEIGHT

  # Only call this function once every FACE_REC_INTERVAL seconds
  if time.time() - last_img_call < FACE_REC_INTERVAL: return
  last_img_call = time.time()
  unscaled_cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
  cv_image = cv2.resize(unscaled_cv_image, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
  last_image = cv_image
  FRAME_WIDTH = last_image.shape[1]
  FRAME_HEIGHT = last_image.shape[0]



def main():
  global last_image, drone_pub, landing_pub
  rospy.init_node("FaceTracker")
  camera_sub = rospy.Subscriber("/bebop/image_raw", Image, img_callback,queue_size=1)
  drone_pub = rospy.Publisher("/bebop/cmd_vel", Twist, queue_size=1)
  takeoff_pub = rospy.Publisher("/bebop/takeoff", Empty, queue_size=1)
  landing_pub = rospy.Publisher("/bebop/land", Empty, queue_size=1)

  camera_pub = rospy.Publisher("/bebop/camera_control", Twist, queue_size=1)

  # Wait until the camera starts giving us frames
  while last_image is None:
    time.sleep(0.5)

  takeoff_pub.publish(Empty())
  time.sleep(2.) # Give the drone time to take off!
  camera_update = Twist()
  camera_update.angular.y = -40
  camera_pub.publish(camera_update)

  start_time = time.time()
  blob_list = []
  last_path_plan = time.time()
  while not rospy.is_shutdown() and time.time() - start_time < FLIGHT_TIME:
    if last_image is not None:
      blob_list = analyzeImage(last_image)
      #debug(blob_list,last_image)
    if(time.time() - last_path_plan > PATH_PLAN_INTERVAL):
      # drone_pub.publish(plan_path(blob_list))
      plan_path(blob_list, drone_pub, landing_pub)
      last_path_plan = time.time()

      last_image = None

      #adjust_drone_pos(face_position)    

  landing_pub.publish(Empty())
  print("Shutdown.")

  cv2.destroyAllWindows()



if __name__ == '__main__':
  bridge = cv_bridge.CvBridge()
  main()
