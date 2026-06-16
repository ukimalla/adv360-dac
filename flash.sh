#!/usr/bin/env bash
# Flash one half of the Adv360 Pro. Put that half into bootloader mode
# first (it mounts as a USB drive), then run:  ./flash.sh left|right [file.uf2]
#
# Bootloader entry (current Kinesis firmware): hold Mod + macro1 (left half)
# or Mod + macro3 (right half); or use the physical reset button (double-tap)
# under each half. The half disconnects as a keyboard and appears as a FAT
# drive containing INFO_UF2.TXT / CURRENT.UF2.
set -euo pipefail

side="${1:-}"; [ "$side" = left ] || [ "$side" = right ] || {
  echo "usage: $0 left|right [path-to.uf2]" >&2; exit 2; }

uf2="${2:-}"
if [ -z "$uf2" ]; then
  # newest matching uf2 in firmware/ or build/
  uf2=$(ls -t firmware/*-"$side".uf2 build/"$side"/zephyr/zmk.uf2 2>/dev/null | head -1 || true)
fi
[ -n "$uf2" ] && [ -f "$uf2" ] || { echo "no .uf2 found for $side (pass one explicitly)" >&2; exit 1; }
echo "[*] flashing $side  <-  $uf2"

find_drive() {
  for base in /run/media/"$USER" /media/"$USER" /media /run/media; do
    [ -d "$base" ] || continue
    while IFS= read -r d; do
      [ -e "$d/INFO_UF2.TXT" ] && { echo "$d"; return 0; }
    done < <(find "$base" -maxdepth 2 -type d 2>/dev/null)
  done
  return 1
}

echo "[*] waiting for the bootloader drive (put $side into bootloader now)..."
drive=""
for _ in $(seq 1 60); do drive=$(find_drive) && break; sleep 1; done
[ -n "$drive" ] || { echo "bootloader drive not found. Is $side in bootloader and mounted?" >&2; exit 1; }

echo "[*] found drive: $drive"
cp -v "$uf2" "$drive"/ && sync || true
echo "[*] done — the half will reboot into the new firmware."
