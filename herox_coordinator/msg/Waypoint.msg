string id                             # Waypoint ID
int32 tagid                           # ID of the AprilTag associated with this waypoint
geometry_msgs/Pose pose               # Pose of the waypoint on the map
geometry_msgs/Pose measurementOffset  # Pose of tag at the waypoint relative to base_link
geometry_msgs/Pose[] shortestPath     # Shortest path to this waypoint from the previous
WaypointVisit[] visits                # Array of visit messages recording data about each visit
