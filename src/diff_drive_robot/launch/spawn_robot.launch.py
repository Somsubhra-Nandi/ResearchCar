import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():

    pkg = get_package_share_directory('diff_drive_robot')

    # ── 1. Parse the xacro into plain URDF XML ──────────────────────
    xacro_file = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # ── 2. Robot State Publisher (broadcasts TF transforms) ─────────
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # ── 3. Launch Gazebo with our world ─────────────────────────────
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4',
             os.path.join(pkg, 'worlds', 'empty_world.sdf')],
        output='screen'
    )

    # ── 4. Spawn the robot into the running Gazebo world ────────────
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-name',  'diff_drive_robot',
            '-topic', 'robot_description',
            '-x', '0', '-y', '0', '-z', '0.1'
        ]
    )

    # ── 5. ROS ↔ Gazebo bridge (clock only for now) ─────────────────
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ]
    )

    return LaunchDescription([
        rsp_node,
        gazebo,
        spawn_robot,
        bridge,
    ])
