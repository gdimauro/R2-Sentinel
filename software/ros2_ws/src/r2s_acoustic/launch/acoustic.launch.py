"""Launch di r2s_acoustic — segnaposto.

Owner: acoustic-perception. Da estendere con i parametri reali.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="r2s_acoustic", executable="listener_node", name="listener_node", output="screen"),
        Node(package="r2s_acoustic", executable="classifier_node", name="classifier_node", output="screen"),
    ])
