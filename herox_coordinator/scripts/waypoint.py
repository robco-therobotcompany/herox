from geometry_msgs.msg import Pose

class Waypoint:
  def __init__(self, pose):
    self.measurements = []
    self.pose = pose
  
  def add_measurement(self, pose):
    self.measurements.append(pose)
