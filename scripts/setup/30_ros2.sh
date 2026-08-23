#!/usr/bin/env bash
# ROS 2 Jazzy da repository ufficiale ros2-apt-source. Idempotente.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
require_ubuntu_2404

if [[ -f /opt/ros/jazzy/setup.bash ]]; then
  skip "ROS 2 Jazzy gia' installato in /opt/ros/jazzy"
else
  apt_install software-properties-common curl ca-certificates
  $SUDO add-apt-repository -y universe >/dev/null

  # Pacchetto ufficiale che porta chiave e sources.list: piu' stabile del
  # `curl | apt-key` che ha rotto le CI di mezzo mondo nel 2024.
  ROS_APT_VER=$(curl -fsSL https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
                | jq -r .tag_name 2>/dev/null || echo "")
  if [[ -n "$ROS_APT_VER" && "$ROS_APT_VER" != "null" ]]; then
    TMPDEB=$(mktemp --suffix=.deb)
    curl -fsSL -o "$TMPDEB" \
      "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_VER}/ros2-apt-source_${ROS_APT_VER#v}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
    $SUDO dpkg -i "$TMPDEB" && rm -f "$TMPDEB"
  else
    warn "impossibile risolvere ros-apt-source, uso il metodo con chiave esplicita"
    $SUDO curl -fsSL -o /usr/share/keyrings/ros-archive-keyring.gpg \
      https://raw.githubusercontent.com/ros/rosdistro/master/ros.key
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) main" \
      | $SUDO tee /etc/apt/sources.list.d/ros2.list >/dev/null
  fi

  $SUDO apt-get update -qq
  APT_UPDATED=1
  apt_install ros-jazzy-ros-base ros-dev-tools python3-colcon-common-extensions \
              python3-rosdep python3-vcstool
  ok "ROS 2 Jazzy installato"
fi

# Pacchetti che i tre consumatori dichiarano in package.xml.
# Nav2 e slam_toolbox pesano: si installano una volta e restano.
apt_install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox \
            ros-jazzy-cv-bridge ros-jazzy-image-transport ros-jazzy-tf2-ros \
            ros-jazzy-rosidl-default-generators ros-jazzy-ament-lint-auto \
            ros-jazzy-ament-cmake ros-jazzy-launch-ros

if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  $SUDO rosdep init >/dev/null 2>&1 || warn "rosdep init gia' fatto"
fi
rosdep update --rosdistro jazzy >/dev/null 2>&1 || warn "rosdep update fallito (offline?)"
ok "rosdep pronto"
