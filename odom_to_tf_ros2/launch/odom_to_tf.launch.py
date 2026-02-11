from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'log_level',
            default_value='info',
            description='Logging level',
        ),
        
        # Odom to TF node - publishes odom->base_link dynamically
        Node(
            package='odom_to_tf_ros2', 
            executable='odom_to_tf',   
            name='odom_to_tf',
            output='screen',
            parameters=[
                {'odom_topic': '/odom_ground_truth'},
                {'use_sim_time': True},
                {'frame_id': 'odom'},
                {'child_frame_id': 'base_link'}
            ],
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        
        # STATIC map->odom transform - Set to (0,0,0) initially
        # The robot's actual position in map frame will be determined by OctoMap origin
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_odom',
            arguments=[
                '6', '6', '0',  # Start at origin, OctoMap will provide offset via map origin
                '0', '0', '0', '1',
                'map',
                'odom'
            ],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
        
        # Static transform for camera mount
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_realsense',
            arguments=[
                '0', '0', '0',
                '0', '0', '0', '1',
                'base_link',
                'realsense'
            ],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
    ])