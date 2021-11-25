#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_srvs.srv import Trigger

joystick_button_states = []

BTN_ESTOP = 1 # B
BTN_ADDWP = 2 # X
BTN_START = 0 # A
BTN_STOP  = 3 # Y

# Returns True if button was pressed, false if not.
# No debouncing, global state array is only updated when button is checked.
# (Function is meant to be executed every loop)
def checkJoystickButton(btn, msg):
  if btn >= msg.buttons:
      print("JOYSTICK_ESTOP: Invalid button number: " + str(btn))
      return False

  # Expand joystick state array if necessary
  while btn >= len(joystick_button_states):
      joystick_button_states.append(msg.buttons[len(joystick_button_states)])

  # Return true if and only if button was pressed
  pressed = not joystick_button_states[btn] and msg.buttons[btn]

  joystick_button_states[btn] = msg.buttons[btn]

  return pressed

def callback(data):
  if checkJoystickButton(BTN_ESTOP, data):
    rospy.loginfo("JOYSTICK_ESTOP: HALT")
    halt()
  if checkJoystickButton(BTN_ADDWP, data):
    addWPService()
  if checkJoystickButton(BTN_START, data):
    startService()
  if checkJoystickButton(BTN_STOP, data):
    stopService()

def joystick_estop():
  global halt
  global startService, stopService, addWPService

  rospy.wait_for_service('/driver/halt')
  halt = rospy.ServiceProxy('/driver/halt', Trigger)
  rospy.init_node('joystick_estop', anonymous=True)
  rospy.Subscriber("/joystick_teleop/joy", Joy, callback)
  startService = rospy.ServiceProxy('/start_mission', Trigger)
  stopService = rospy.ServiceProxy('/stop_mission', Trigger)
  addWPService = rospy.ServiceProxy('/add_waypoint', Trigger)
  rospy.spin()

if __name__ == '__main__':
  try:
    joystick_estop()
  except rospy.ROSInterruptException:
    pass
