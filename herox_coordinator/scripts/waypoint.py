from geometry_msgs.msg import Pose
from herox_coordinator.msg import Waypoint, WaypointVisit

class MissionWaypoint:
  def __init__(self, pose = None, waypoint_id = None, tag = None):
    self.tag = tag
    self.measurements = []
    self.pose = pose
    self.shortest_path = []
    self.visits = []
    self.waypoint_id = waypoint_id
 
  def add_measurement(self, pose):
    self.measurements.append(pose)

  def add_pose_to_path(self, pose):
    if self.visits > len(self.actual_paths):
      self.actual_paths.append([pose])
    else:
      self.actual_paths[self.visits - 1].append(pose)

  def set_shortest_path(self, poses):
    self.shortest_path = poses.copy()

  def increment_visits(self):
    self.visits = self.visits + 1

  def write_to_bag(self, bag):
    wp = Waypoint()
    wp.id = self.waypoint_id
    wp.pose = self.pose
    wp.shortestPath = self.shortest_path
    wp.visits = self.visits
    wp.tagname = self.tag
    bag.write('mission_waypoints', wp)

  def load_from_bag(self, msg):
    self.waypoint_id = msg.id
    self.pose = msg.pose
    self.shortestPath = msg.shortestPath
    self.visits = msg.visits
    self.tag = msg.tagname
