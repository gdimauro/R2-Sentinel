#!/usr/bin/env bash
# Dipendenze di sistema, Ubuntu 24.04. Idempotente.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

require_ubuntu_2404

PKGS=(
  build-essential cmake git curl wget gnupg2 lsb-release ca-certificates
  python3 python3-pip python3-venv python3-dev
  # ESP-IDF
  flex bison gperf ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
  # utilita' di piattaforma
  jq unzip pkg-config udev
)
apt_install "${PKGS[@]}"

# Regole udev per ESP32 senza sudo: senza questo il flash "non funziona"
# e la causa e' sempre la stessa, quindi si risolve una volta per tutti.
if [[ -w /etc/udev/rules.d ]] || sudo_available; then
  if [[ ! -f /etc/udev/rules.d/99-r2s-esp32.rules ]]; then
    $SUDO tee /etc/udev/rules.d/99-r2s-esp32.rules >/dev/null <<'RULES'
# ESP32-S3 (USB-JTAG/serial nativo e CP210x/CH340 delle devkit)
SUBSYSTEM=="usb", ATTR{idVendor}=="303a", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", MODE="0666", GROUP="dialout"
RULES
    $SUDO udevadm control --reload-rules 2>/dev/null || true
    ok "regole udev ESP32 installate"
  else
    skip "regole udev gia' presenti"
  fi
  $SUDO usermod -aG dialout "$USER" 2>/dev/null || true
fi
ok "dipendenze di sistema a posto"
