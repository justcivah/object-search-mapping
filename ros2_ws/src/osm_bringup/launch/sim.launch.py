from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('world', default_value='boxes',
                          description='World name, only used in simulation'),
    # not 'rviz': launch configurations are shared with included files, and
    # clearpath uses 'rviz' to open its own rviz window
    DeclareLaunchArgument('use_rviz', default_value='true',
                          choices=['true', 'false'], description='Start rviz.'),
    DeclareLaunchArgument('namespace', default_value='a200_0000',
                          description='Robot namespace (from clearpath/robot.yaml)'),
]


def generate_launch_description():
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('osm_simulation'), 'launch', 'simulation.launch.py'])),
        launch_arguments=[
            ('world', LaunchConfiguration('world')),
            ('use_sim_time', 'true'),
            ('rviz', 'false'),
        ],
    )

    # slam and nav2 both declare 'params_file': scoped groups keep each value
    # inside its own include (safe here, unlike the clearpath simulation include,
    # since these launch files have no delayed event handlers)
    slam = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([FindPackageShare('osm_navigation'), 'launch', 'slam.launch.py'])),
            launch_arguments=[
                ('namespace', LaunchConfiguration('namespace')),
                ('use_sim_time', 'true'),
            ],
        ),
    ])

    nav2 = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([FindPackageShare('osm_navigation'), 'launch', 'nav2.launch.py'])),
            launch_arguments=[
                ('namespace', LaunchConfiguration('namespace')),
                ('use_sim_time', 'true'),
            ],
        ),
    ])
    
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        namespace=LaunchConfiguration('namespace'),
        arguments=['-d', PathJoinSubstitution([FindPackageShare('osm_bringup'), 'rviz', 'sim.rviz'])],
        parameters=[{'use_sim_time': True}],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
        ],
        condition=IfCondition(LaunchConfiguration('use_rviz')),
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(simulation)
    ld.add_action(slam)
    ld.add_action(nav2)
    ld.add_action(rviz)
    return ld
