string id                             # Waypoint ID
string tagname                        # Name of the AprilTag associated with this waypoint
geometry_msgs/Pose pose               # Pose of the waypoint on the map
geometry_msgs/Pose measurementOffset  # Pose of robot at the waypoint relative to apriltag
geometry_msgs/Pose[] shortestPath     # Shortest path to this waypoint from the previous
WaypointVisit[] visits                # Array of visit messages recording data about each visit
