#!/usr/bin/env bash
set -euo pipefail
cd /workspace
echo "[*] west init"; west init -l config 2>&1 | tail -2 || true
echo "[*] west update (downloading zephyr/zmk modules, may take minutes)"; west update 2>&1 | tail -5
echo "[*] west zephyr-export"; west zephyr-export 2>&1 | tail -2
echo "[*] build LEFT"; west build -s zmk/app -d build/left -b adv360_left -- -DZMK_CONFIG=/workspace/config 2>&1 | tail -25
echo "[*] build RIGHT"; west build -s zmk/app -d build/right -b adv360_right -- -DZMK_CONFIG=/workspace/config 2>&1 | tail -25
echo "[*] artifacts:"; ls -la build/left/zephyr/zmk.uf2 build/right/zephyr/zmk.uf2
