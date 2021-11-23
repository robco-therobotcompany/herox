import rospy
import rosbag
from waypoint import MissionWaypoint
from geometry_msgs.msg import Pose

class Mission:
  benchmark = False # True  = benchmark mode, paths are recorded and measurements taken at every waypoint
                    # False = mission-only mode, mission is executed without evaluation

  def __init__(self, bag = None):
    self.waypoints = []
    self.currentGoal = -1

    if bag is not None:
      self.load_from_bag(bag)
      self.name = bag.filename

  def set_benchmark_mode(self, benchmark_mode):
    self.benchmark = benchmark_mode

  def add_waypoint(self, pose):
    self.waypoints.append(MissionWaypoint(pose, waypoint_id = len(self.waypoints), tag = "mytag"))

  def get_current_waypoint(self):
    return self.waypoints[self.currentGoal]

  def next_waypoint(self):
    self.currentGoal = self.currentGoal + 1
    if self.currentGoal >= len(self.waypoints):
      self.currentGoal = len(self.waypoints)
      return None

    if self.benchmark:
      self.waypoints[self.currentGoal].increment_visits()

    return self.waypoints[self.currentGoal]

  def add_measurement(self, pose):
    self.waypoints[self.currentGoal].add_measurement(pose)

  def reset(self, start_at=0):
    self.currentGoal = start_at - 1

  def load_from_bag(self, bag):
    self.waypoints = []
    for topic, msg, t in bag.read_messages(topics=['mission_waypoints']):
      rospy.loginfo("Loaded waypoint: %f,%f,%f %f,%f,%f,%f", msg.pose.position.x, msg.pose.position.y,
                                                             msg.pose.position.z, msg.pose.orientation.x,
                                                             msg.pose.orientation.y, msg.pose.orientation.z,
                                                             msg.pose.orientation.w)
      wp = MissionWaypoint()
      wp.load_from_bag(msg)
      self.waypoints.append(wp)

  def save_to_bag(self, bag):
    for wp in self.waypoints:
      wp.write_to_bag(bag)
