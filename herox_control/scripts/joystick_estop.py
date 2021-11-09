#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_srvs.srv import Trigger

def callback(data):
  if len(data.buttons) >= 1 and data.buttons[1]:
    rospy.loginfo("JOYSTICK_ESTOP: HALT")
    halt()

def joystick_estop():
  global halt

  rospy.wait_for_service('/driver/halt')
  halt = rospy.ServiceProxy('/driver/halt', Trigger)
  rospy.init_node('joystick_estop', anonymous=True)
  rospy.Subscriber("/joystick_teleop/joy", Joy, callback)
  rospy.spin()

if __name__ == '__main__':
  try:
    joystick_estop()
  except rospy.ROSInterruptException:
    pass
