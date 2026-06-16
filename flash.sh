#!/usr/bin/env bash
# Flash one half of the Adv360 Pro. Put that half into bootloader mode
# first (double-tap its physical reset button; it mounts as a UF2 drive),
# then run:  ./flash.sh left|right [file.uf2]
#
# Auto-detects + mounts the bootloader drive via udisksctl (no desktop
# automounter required) and copies the firmware.
set -euo pipefail

side="${1:-}"; [ "$side" = left ] || [ "$side" = right ] || {
  echo "usage: $0 left|right [path-to.uf2]" >&2; exit 2; }

uf2="${2:-}"
if [ -z "$uf2" ]; then
  uf2=$(ls -t firmware/adv360-"$side".uf2 firmware/*-"$side".uf2 \
           build/"$side"/zephyr/zmk.uf2 2>/dev/null | head -1 || true)
fi
[ -n "$uf2" ] && [ -f "$uf2" ] || { echo "no .uf2 found for $side (pass one explicitly)" >&2; exit 1; }
echo "[*] flashing $side  <-  $uf2"

# Returns the mountpoint of a UF2 bootloader volume, mounting it if needed.
find_uf2_mount() {
  # already-mounted UF2 volume?
  for mp in $(lsblk -rno MOUNTPOINT 2>/dev/null | grep -v '^$'); do
    [ -e "$mp/INFO_UF2.TXT" ] && { echo "$mp"; return 0; }
  done
  # try to mount removable vfat partitions and check
  while read -r name fstype rm; do
    [ "$fstype" = vfat ] || continue
    [ "$rm" = 1 ] || continue
    dev="/dev/$name"
    mp=$(lsblk -rno MOUNTPOINT "$dev" 2>/dev/null | head -1)
    if [ -z "$mp" ]; then
      mp=$(udisksctl mount -b "$dev" 2>/dev/null | sed -n 's/.* at \(.*\)\.\?$/\1/p' | tr -d '.')
    fi
    [ -n "$mp" ] && [ -e "$mp/INFO_UF2.TXT" ] && { echo "$mp"; return 0; }
  done < <(lsblk -rno NAME,FSTYPE,RM 2>/dev/null)
  return 1
}

echo "[*] waiting for the $side bootloader drive — double-tap its reset button now..."
drive=""
for _ in $(seq 1 90); do drive=$(find_uf2_mount) && break; sleep 1; done
[ -n "$drive" ] || { echo "bootloader drive not found. Is $side in bootloader?" >&2; exit 1; }

echo "[*] found UF2 drive at: $drive"
cp -v "$uf2" "$drive"/ 2>/dev/null || cp -v "$uf2" "$drive"/ || true
sync 2>/dev/null || true
echo "[*] done — $side will reboot into the new firmware (the drive disconnects)."
