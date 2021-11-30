import rospy
from geometry_msgs.msg import Pose
from herox_coordinator.msg import Waypoint, WaypointVisit

class MissionWaypoint:
  def __init__(self, pose = None, waypoint_id = None, tag = None, pose_reference = None):
    self.tag = tag
    self.pose = pose
    self.pose_reference = pose_reference
    self.shortest_path = []
    self.visits = []
    self.current_path = []
    self.waypoint_id = waypoint_id
 
  def add_visit(self, pose):
    visit = WaypointVisit()
    visit.stamp = rospy.Time.now()
    visit.measurement = pose
    visit.path = self.current_path
    self.current_path = []
    self.visits.append(visit)

  def add_pose_to_path(self, pose):
    self.current_path.append(pose)

  def set_shortest_path(self, poses):
    self.shortest_path = poses

  def increment_visits(self):
    self.visits = self.visits + 1

  def get_msg(self):
    wp = Waypoint()
    wp.id = self.waypoint_id
    wp.pose = self.pose
    wp.shortestPath = self.shortest_path
    wp.visits = self.visits
    wp.tagid = self.tag
    wp.measurementOffset = self.pose_reference
    return wp

  def load_from_msg(self, msg):
    self.waypoint_id = msg.id
    self.pose = msg.pose
    self.shortestPath = msg.shortestPath
    self.visits = msg.visits
    self.pose_reference = msg.measurementOffset
    self.tag = msg.tagid
