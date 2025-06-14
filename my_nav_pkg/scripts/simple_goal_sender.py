#!/usr/bin/env python3
"""
Send a (x, y, yaw) goal to move_base and wait for the result.
"""

import math, rospy, actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler

def build_goal(x, y, yaw_deg):
    q = quaternion_from_euler(0, 0, math.radians(yaw_deg))
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose = Pose(
        position=Point(x=x, y=y, z=0),
        orientation=Quaternion(x=q[0], y=q[1], z=q[2], w=q[3]))
    return goal

if __name__ == "__main__":
    rospy.init_node("simple_goal_sender")
    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("Waiting for move_base server…")
    client.wait_for_server()

    goal = build_goal(1.0, -0.5, 90)       # <- change as you like
    rospy.loginfo("Sending goal %s", goal.target_pose.pose.position)
    client.send_goal(goal)

    if client.wait_for_result(rospy.Duration(120)):
        if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("✅ Goal reached!")
        else:
            rospy.logwarn("⚠️  move_base failed with status %d", client.get_state())
    else:
        rospy.logwarn("⏰ Timeout; cancelling goal")
        client.cancel_goal()
