from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='a200_0000',
                          description='Robot namespace (from clearpath/robot.yaml)'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('params_file',
                          default_value=PathJoinSubstitution(
                              [get_package_share_directory('osm_navigation'), 'config', 'slam.yaml']),
                          description='slam_toolbox parameters file'),
]


def generate_launch_description():
    # online async mode, scans are dropped if processing falls behind
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        namespace=LaunchConfiguration('namespace'),
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        # remappings relative to the husky namespace
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
            ('/map', 'map'),
            ('/map_metadata', 'map_metadata'),
        ],
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(slam_toolbox)
    return ld
