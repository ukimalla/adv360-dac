#!/usr/bin/env bash
# Guided flash of both Adv360 Pro halves. Run interactively:
#     ! ~/Projects/keyb/adv360-dac/flash-both.sh
# It walks you through putting each half into bootloader and copies the
# firmware (mounting the UF2 drive via udisksctl; you may be asked for your
# password once per half, since this is over SSH).
set -uo pipefail
cd "$(dirname "$(readlink -f "$0")")"

for side in left right; do
  echo
  echo "============================================================"
  echo ">>> Put the  $side  half into BOOTLOADER mode now:"
  if [ "$side" = left ]; then
    echo "      • on stock firmware:  Mod + Hotkey 1"
  else
    echo "      • on stock firmware:  Mod + Hotkey 3"
  fi
  echo "      • or double-click the recessed RESET pinhole (paperclip) in the"
  echo "        $side thumb cluster, where 3 thumb keys meet."
  echo "    The half must be USB-connected; a USB drive appears in bootloader."
  echo "============================================================"
  read -rp "Press ENTER once the $side half is in bootloader... " _
  if ./flash.sh "$side"; then
    echo "[ok] $side flashed."
  else
    echo "[!] $side flash did not complete — see message above."
    read -rp "Retry $side? [y/N] " r
    [ "$r" = y ] && ./flash.sh "$side" || echo "skipping $side"
  fi
done

echo
echo "Done. Both halves reboot into the new firmware and should re-pair."
echo "If they don't talk to each other, see UPGRADE.md / Kinesis settings-reset."
