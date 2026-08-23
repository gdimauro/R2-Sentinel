"""Launch di r2s_vision — segnaposto.

Owner: vision-perception. Da estendere con i parametri reali.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="r2s_vision", executable="detector_node", name="detector_node", output="screen"),
        Node(package="r2s_vision", executable="calibration_node", name="calibration_node", output="screen"),
    ])
