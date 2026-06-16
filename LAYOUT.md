# Adv360 Pro — dactyl `dac` layout port

This config replicates my 8-layer Dactyl Manuform **`dac`** ZMK keymap
(`github.com/ukimalla/zmk-dactyl-manuform`) on the Kinesis Advantage 360
Pro. The dactyl is a 5×6 Manuform with a 7-key thumb cluster per hand
(62 keys); the Adv360 LAYOUT has 76 positions. `gen_keymap.py` holds the
exact position mapping and regenerates `config/adv360.keymap`.

## Base layer (layer 0)

```
LEFT                                    RIGHT
GESC  1  2  3  4  5                      6  7  8  9  0  -
TAB   Q  W  E  R  T                      Y  U  I  O  P  \
LSFT  A  S  D  F  G                      H  J  K  L  ;  '
CTL/CAPS Z X C V B                       N  M  ,  .  /  =
(bottom row, Adv360-only):              (bottom row, Adv360-only):
  [CTL/[]  `  CAPS  ←  →                   ↑  ↓  [  ]  [CTL/]]
```

`GESC` = grave/escape (`&gresc`). `CTL/CAPS` = Ctrl held / Caps tapped.
The two bottom corner keys carry the dactyl thumb mod-taps that didn't
fit the Adv360 thumb cluster: left corner = `Ctrl`/`[`, right = `Ctrl`/`]`.

### Thumb clusters

| Adv360 key            | Left thumb        | Right thumb        |
|-----------------------|-------------------|--------------------|
| upper small (×2)      | `LGUI`, `LALT`    | `RGUI`, `Alt/AltGr`|
| arc key               | `L5`/`Home`       | `PgUp`             |
| big primary (×2)      | `L2`/`Del`, `L4`/`Enter` | `Bksp`, `Space` |
| inner key             | `L6`/`End`        | `PgDn`             |

`Ln`/`Key` = layer-tap: hold for layer *n*, tap for the key. All four
layer-taps live on the left thumb, exactly as on the dactyl.

## Layers

| # | Name  | Reached by            | Contents |
|---|-------|-----------------------|----------|
| 0 | Base  | —                     | QWERTY (above) |
| 1 | —     | (unused, transparent) | matches dactyl's empty layer |
| 2 | Num   | hold left-thumb **Del**   | F1–F12, numpad cluster, brackets |
| 3 | —     | (unused, transparent) | |
| 4 | Nav   | hold left-thumb **Enter** | arrows, Home/End/PgUp/PgDn, browser tab/ws shortcuts, Insert, PrtSc, Menu |
| 5 | Media | hold left-thumb **Home**  | volume, prev/play/next, mute |
| 6 | Mouse | hold left-thumb **End**   | mouse move/scroll/click (`&mmv`/`&msc`/`&mkp`) |
| 7 | Reset | hold the `mo 7` key on Media/Mouse | `&bootloader` |
| 8 | Sys   | hold the upper-inner-right key | BT select 0–4 / clear, RGB & backlight toggle, bootloader, ZMK Studio unlock |

Layer 8 ("Sys") is **new** — the dactyl had no equivalent. It lives on an
Adv360-only key so it doesn't disturb dactyl muscle memory, and it keeps
Bluetooth pairing, RGB/backlight, and re-flashing reachable.

Keys the original dactyl config left deliberately dead use `&kp F20`
(a no-op F-key), preserved here verbatim.

## Building & flashing

- **CI:** push to `main`; GitHub Actions builds `…-left.uf2` / `…-right.uf2`
  (download from the run's artifacts).
- **Local:** `docker run --rm -v "$PWD":/workspace -w /workspace \
  zmkfirmware/zmk-build-arm:stable ./build.sh` → `build/{left,right}/zephyr/zmk.uf2`.
- **Flash:** put a half into bootloader (Mod+macro1 = left, Mod+macro3 =
  right, or the physical reset button), then `./flash.sh left|right`.
  See `README.md` → "Flashing firmware" for the official procedure.
