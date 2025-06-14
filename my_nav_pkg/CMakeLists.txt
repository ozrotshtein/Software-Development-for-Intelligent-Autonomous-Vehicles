cmake_minimum_required(VERSION 3.0.2)
project(my_nav_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy geometry_msgs move_base_msgs actionlib tf
)

catkin_package()

install(PROGRAMS
  scripts/simple_goal_sender.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
