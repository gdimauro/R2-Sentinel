"""Launch di r2s_mqtt_bridge — segnaposto.

Owner: software-platform. Da estendere con i parametri reali.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="r2s_mqtt_bridge", executable="bridge_node", name="bridge_node", output="screen"),
        Node(package="r2s_mqtt_bridge", executable="topic_lint", name="topic_lint", output="screen"),
    ])
