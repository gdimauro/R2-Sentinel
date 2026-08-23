#!/usr/bin/env bash
# Build del workspace ROS 2. E' il passo che dice se il bootstrap e' riuscito.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WS="$ROOT/software/ros2_ws"

[[ -f /opt/ros/jazzy/setup.bash ]] || die "ROS 2 Jazzy non trovato: esegui prima il passo 'ros'"
# shellcheck disable=SC1091
set +u; . /opt/ros/jazzy/setup.bash; set -u

cd "$WS"
if command -v rosdep >/dev/null 2>&1; then
  rosdep install --from-paths src --ignore-src -y --rosdistro jazzy \
    || warn "rosdep non ha risolto tutto: alcuni pacchetti potrebbero mancare"
fi

colcon build --symlink-install --event-handlers console_direct+ \
  --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
ok "workspace compilato"

# shellcheck disable=SC1091
set +u; . "$WS/install/setup.bash"; set -u
for p in r2s_interfaces r2s_vision r2s_acoustic r2s_navigation r2s_mqtt_bridge r2s_bringup; do
  ros2 pkg list | grep -qx "$p" || die "pacchetto non trovato dopo la build: $p"
done
ok "6/6 pacchetti r2s_* visibili a ros2 pkg list"
