"""Launch di r2s_navigation — segnaposto.

Owner: autonomy. Da estendere con i parametri reali.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="r2s_navigation", executable="docking_node", name="docking_node", output="screen"),
        Node(package="r2s_navigation", executable="recovery_node", name="recovery_node", output="screen"),
    ])
