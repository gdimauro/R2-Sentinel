# Immagine di CI: Ubuntu 24.04 con ROS 2 Jazzy gia' dentro, per non pagare
# l'installazione a ogni PR (budget CI: <= 10 min).
# NON e' l'immagine con cui si verifica la riproducibilita': quella e'
# ubuntu2404-clean.Dockerfile, che parte davvero da zero.
FROM ros:jazzy-ros-base-noble

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
        git git-lfs curl jq python3-venv python3-pip \
        python3-colcon-common-extensions python3-rosdep \
        ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox \
        ros-jazzy-cv-bridge ros-jazzy-image-transport ros-jazzy-tf2-ros \
        ros-jazzy-ament-lint-auto ros-jazzy-ament-cmake-lint-cmake \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install --skip-repo
WORKDIR /ws
