cmake_minimum_required(VERSION 3.8)
project(diff_drive_robot)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# Install all resource folders
install(DIRECTORY
  urdf launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
