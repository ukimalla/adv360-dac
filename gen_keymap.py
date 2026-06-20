#!/usr/bin/env python3
"""Generate config/adv360.keymap from the real `zdac` shield keymap.

zdac is a dactyl-manuform-wired DACTYL: 70 keys = a 5-row 6-col main grid
per hand + a 6-key thumb cluster per hand. We parse zdac.keymap directly
(all 8 layers) and remap each position onto the Adv360 Pro's 76-key LAYOUT.

The thumb mapping is from Q's spec (left, by original-Kinesis key) mirrored
to the right:
  Adv360 stock key  ->  zdac binding
  LALT  -> lt4 HOME      LGUI(R) -> mt LCTRL ESC
  LCTRL -> lt5 HOME      RCTRL   -> PG_UP
  HOME  -> lt6 END       PG_UP   -> PG_DN
  BSPC  -> SPACE         SPACE   -> lt4 ENTER
  DEL   -> BACKSPACE     ENTER   -> lt2 DEL
  END   -> mt LCTRL [    PG_DN   -> mt RCTRL ]
zdac's 5th row maps to the Adv360 bottom row; zdac's omitted N6/N7 go on
the two spare Adv360 inner-top keys.
"""
import re, sys

ZDAC = "/run/media/ukimalla/a463f878-2390-4952-8482-e168c97bd878/home/ukimalla/zmk-dactyl_manuform/zmk/app/boards/shields/zdac/zdac.keymap"

# ---- parse all layers from zdac.keymap -------------------------------------
src = open(ZDAC).read()
layers = []
for m in re.finditer(r'layer\d+\s*\{.*?bindings\s*=\s*<(.*?)>\s*;', src, re.S):
    body = m.group(1)
    toks = ["&" + t.strip() for t in body.split("&") if t.strip()]
    layers.append(toks)

if len(layers) != 8:
    sys.exit(f"expected 8 zdac layers, parsed {len(layers)}")
for i, l in enumerate(layers):
    if len(l) != 70:
        sys.exit(f"zdac layer {i} has {len(l)} tokens, expected 70")

# fix up a couple of keycodes for ZMK
def fix(tok):
    return tok.replace("K_APPLICATION", "K_APP")
layers = [[fix(t) for t in l] for l in layers]

# ---- Adv360 LAYOUT index  <-  zdac position --------------------------------
ADV_TO_ZDAC = {
    # row0  (ESC 1 2 3 4 5 | boot reset 8 9 0 -)
    0:0,1:1,2:2,3:3,4:4,5:5, 8:6,9:7,10:8,11:9,12:10,13:11,
    # row1
    14:12,15:13,16:14,17:15,18:16,19:17, 22:18,23:19,24:20,25:21,26:22,27:23,
    # row2
    28:24,29:25,30:26,31:27,32:28,33:29, 40:30,41:31,42:32,43:33,44:34,45:35,
    # row3
    46:36,47:37,48:38,49:39,50:40,51:41, 54:42,55:43,56:44,57:45,58:46,59:47,
    # 5th row -> Adv360 bottom row
    60:48,61:49,62:50,63:51,64:52,   71:55,72:56,73:57,74:58,75:59,
    # left thumb
    65:53,  66:60,  35:62,  36:61,  52:66,  67:68,
    # right thumb
    70:54,  69:65,  38:63,  37:64,  53:67,  68:69,
}
HOLES = {20, 21, 34, 39}              # disabled matrix positions -> &none
# spare Adv360 inner-top keys: restore zdac's omitted N6/N7 on the base layer
BASE_EXTRA = {6: "&kp N6", 7: "&kp N7"}


def build(layer, is_base):
    out = []
    for adv in range(76):
        if adv in ADV_TO_ZDAC:
            out.append(layer[ADV_TO_ZDAC[adv]])
        elif adv in HOLES:
            out.append("&none")
        elif is_base and adv in BASE_EXTRA:
            out.append(BASE_EXTRA[adv])
        else:
            out.append("&trans")
    return out


def fmt(t):
    rows = [(0,14),(14,28),(28,46),(46,60),(60,76)]
    return "\n".join("        " + " ".join(t[a:b]) for a,b in rows)

NAMES = ["Base","L1","Num","L3","Nav","Media","Mouse","Reset"]
HEADER = '''#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/rgb.h>
#include <dt-bindings/zmk/backlight.h>

/ {
    keymap {
        compatible = "zmk,keymap";
'''
TMPL = '''
        layer_{n} {{
            display-name = "{name}";
            bindings = <
{body}
            >;
        }};
'''
parts = [HEADER]
for n,(lay,name) in enumerate(zip(layers, NAMES)):
    parts.append(TMPL.format(n=n, name=name, body=fmt(build(lay, n==0))))
parts.append("    };\n};\n")
open("config/adv360.keymap","w").write("".join(parts))
print("wrote config/adv360.keymap  (8 layers from zdac, 76 keys each)")
