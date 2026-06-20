#!/usr/bin/env bash
set -euo pipefail
cd /workspace
echo "[*] west init"; west init -l config 2>&1 | tail -2 || true
echo "[*] west update"; west update 2>&1 | tail -5
echo "[*] west zephyr-export"; west zephyr-export 2>&1 | tail -2
# Left/central: build WITH ZMK Studio (studio-rpc-usb-uart snippet supplies
# the zmk,studio-rpc-uart chosen node + USB CDC transport).
echo "[*] build LEFT (+ZMK Studio)"
west build -p -s zmk/app -d build/left  -b adv360_left  -S studio-rpc-usb-uart \
  -- -DZMK_CONFIG=/workspace/config -DCONFIG_ZMK_STUDIO=y 2>&1 | tail -8
echo "[*] build RIGHT"
west build -p -s zmk/app -d build/right -b adv360_right \
  -- -DZMK_CONFIG=/workspace/config 2>&1 | tail -8
echo "[*] artifacts:"; ls -la build/left/zephyr/zmk.uf2 build/right/zephyr/zmk.uf2
