from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare


ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='a200_0000',
                          description='Robot namespace (from clearpath/robot.yaml)'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('params_file',
                          default_value=PathJoinSubstitution(
                              [get_package_share_directory('osm_navigation'), 'config', 'nav2.yaml']),
                          description='Nav2 parameters file'),
]


def generate_launch_description():
    # navigation_launch.py starts planner, controller, behaviors and bt_navigator,
    # but no map_server/amcl: map and map -> odom come from slam_toolbox.
    # It does not push the namespace itself (bringup_launch.py does), so we do it
    # here; it already remaps /tf and nests the params file under the namespace
    nav2 = GroupAction([
        PushRosNamespace(LaunchConfiguration('namespace')),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([FindPackageShare('nav2_bringup'), 'launch', 'navigation_launch.py'])),
            launch_arguments=[
                ('namespace', LaunchConfiguration('namespace')),
                ('use_sim_time', LaunchConfiguration('use_sim_time')),
                ('params_file', LaunchConfiguration('params_file')),
                ('autostart', 'true'),
            ],
        ),
    ])

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(nav2)
    return ld
