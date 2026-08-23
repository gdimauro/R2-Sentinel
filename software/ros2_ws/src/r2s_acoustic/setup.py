from setuptools import find_packages, setup
from glob import glob
import os

package_name = "r2s_acoustic"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="R2-Sentinel",
    maintainer_email="gdimauro@codearchitects.com",
    description="Percezione acustica Unita' B: microfono I2S 48 kHz, FFT, classificatore",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "listener_node = r2s_acoustic.listener_node:main",
            "classifier_node = r2s_acoustic.classifier_node:main",
        ],
    },
)
