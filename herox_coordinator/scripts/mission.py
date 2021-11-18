import rospy
import rosbag
from waypoint import Waypoint
from geometry_msgs.msg import Pose

class Mission:
  def __init__(self, bag = None):
    self.waypoints = []
    self.currentGoal = -1

    if bag is not None:
      self.load_from_bag(bag)
      self.name = bag.filename

  def add_waypoint(self, pose):
    self.waypoints.append(Waypoint(pose))

  def next_waypoint(self):
    self.currentGoal = self.currentGoal + 1
    if self.currentGoal >= len(self.waypoints):
      return None

    return self.waypoints[self.currentGoal]

  def reset(self, start_at=0):
    self.currentGoal = start_at - 1

  def load_from_bag(self, bag):
    self.waypoints = []
    for topic, msg, t in bag.read_messages(topics=['mission_waypoints']):
      rospy.loginfo("Loaded waypoint: %f,%f,%f %f,%f,%f,%f", msg.position.x, msg.position.y, msg.position.z, msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)
      self.waypoints.append(Waypoint(msg))

  def save_to_bag(self, bag):
    for wp in self.waypoints:
      bag.write('mission_waypoints', wp.pose)
