"""Unita' B — interno, mobile (§4.3).

Composizione: acustica + navigazione + bridge MQTT.
"""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        DeclareLaunchArgument("mqtt_host", default_value="127.0.0.1"),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare("r2s_acoustic"), "launch", "acoustic.launch.py"]))),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare("r2s_navigation"), "launch", "navigation.launch.py"]))),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare("r2s_mqtt_bridge"), "launch", "mqtt_bridge.launch.py"])),
            launch_arguments={"mqtt_host": LaunchConfiguration("mqtt_host")}.items()),
    ])
