import rospy
import rosbag
from waypoint import MissionWaypoint
from geometry_msgs.msg import Pose
import herox_coordinator.msg as cmsg
import os

class Mission:
  benchmark = False # True  = benchmark mode, paths are recorded and measurements taken at every waypoint
                    # False = mission-only mode, mission is executed without evaluation
  name = ""

  def __init__(self, bag = None):
    self.waypoints = []
    self.currentGoal = -1

    if bag is not None:
      self.load_from_bag(bag)

  def set_benchmark_mode(self, benchmark_mode):
    self.benchmark = benchmark_mode

  def add_waypoint(self, pose, tag, measurement):
    wp = MissionWaypoint(pose, waypoint_id = str(len(self.waypoints)), tag = tag, pose_reference = measurement)
    self.waypoints.append(wp)

  def get_current_waypoint(self):
    if self.currentGoal >= 0 and self.currentGoal < len(self.waypoints):
      return self.waypoints[self.currentGoal]

  def next_waypoint(self):
    self.currentGoal = self.currentGoal + 1
    if self.currentGoal >= len(self.waypoints):
      self.currentGoal = len(self.waypoints)
      return None

    if self.benchmark:
      self.waypoints[self.currentGoal].increment_visits()

    return self.waypoints[self.currentGoal]

  def add_visit(self, pose):
    self.waypoints[self.currentGoal].add_visit(pose)

  def add_pose_to_path(self, pose):
    self.waypoints[self.currentGoal].add_pose_to_path(pose)

  def reset(self, start_at=0):
    self.currentGoal = start_at - 1

  def load_from_bag(self, bag):
    self.waypoints = []
    for topic, miss, t in bag.read_messages(topics=['mission']):
      self.name = miss.name
      for msg in miss.waypoints:
        rospy.loginfo("Loaded waypoint: %f,%f,%f %f,%f,%f,%f", msg.pose.position.x, msg.pose.position.y,
                                                             msg.pose.position.z, msg.pose.orientation.x,
                                                             msg.pose.orientation.y, msg.pose.orientation.z,
                                                             msg.pose.orientation.w)
        wp = MissionWaypoint()
        wp.load_from_msg(msg)
        self.waypoints.append(wp)
      break

  def save_to_bag(self, bag):
    msg = cmsg.Mission()
    msg.name = self.name
    msg.waypoints = []
    for wp in self.waypoints:
      msg.waypoints.append(wp.get_msg())
    bag.write('mission',msg)
