#!/usr/bin/env python3
"""Generate config/adv360.keymap from the dactyl `dac` layout.

The dactyl `dac` shield is a 5x6 Dactyl Manuform with a 7-key thumb
cluster per hand (62 keys). The Adv360 Pro LAYOUT has 76 positions:
a 6x4 main grid per hand, an extra inner key per hand on the top row,
a full extra bottom row, four disabled matrix holes, and a 6-key thumb
cluster per hand. We map the dactyl bindings onto the Adv360 positions,
translating the dactyl's leftover QMK keycodes into real ZMK behaviors.
"""

# ---- Adv360 LAYOUT position -> dactyl binding index --------------------
# Adv360 indices are in LAYOUT order, grouped 14/14/18/14/16 per row.
ADV_TO_DAC = {
    # row0 numbers
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
    8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 11,
    # row1 QWERTY top
    14: 12, 15: 13, 16: 14, 17: 15, 18: 16, 19: 17,
    22: 18, 23: 19, 24: 20, 25: 21, 26: 22, 27: 23,
    # row2 home
    28: 24, 29: 25, 30: 26, 31: 27, 32: 28, 33: 29,
    40: 30, 41: 31, 42: 32, 43: 33, 44: 34, 45: 35,
    # row3 bottom alpha
    46: 36, 47: 37, 48: 38, 49: 39, 50: 40, 51: 41,
    54: 42, 55: 43, 56: 44, 57: 45, 58: 46, 59: 47,
    # thumbs (left): LGUI LALT lt5/HOME lt2/DEL lt4/ENTER lt6/END mt LCTRL/LBKT
    35: 48, 36: 49, 52: 52, 65: 54, 66: 55, 67: 59, 60: 58,
    # thumbs (right): RGUI mt LALT/RALT PG_UP PG_DN BSPC SPACE mt RCTRL/RBKT
    37: 57, 38: 56, 53: 53, 68: 60, 69: 51, 70: 50, 75: 61,
}

# Adv360-only positions. 20/21/34/39 are disabled matrix holes -> &none.
HOLES = {20, 21, 34, 39}
# Bonus keys the dactyl lacks; on base they get useful Adv360 defaults.
BASE_EXTRA = {
    6: "&trans", 7: "&mo 8",
    61: "&kp GRAVE", 62: "&kp CAPS", 63: "&kp LEFT", 64: "&kp RIGHT",
    71: "&kp UP", 72: "&kp DOWN", 73: "&kp LBKT", 74: "&kp RBKT",
}

F20 = "&kp F20"  # the dactyl uses F20 as a deliberate "dead" key

# ---- dactyl layers (62 tokens each), QMK already translated to ZMK -----
L0 = (
    ["&gresc"] + [f"&kp N{n}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)] + ["&kp MINUS"] +
    ["&kp TAB", "&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
     "&kp Y", "&kp U", "&kp I", "&kp O", "&kp P", "&kp BSLH"] +
    ["&kp LSHFT", "&kp A", "&kp S", "&kp D", "&kp F", "&kp G",
     "&kp H", "&kp J", "&kp K", "&kp L", "&kp SEMI", "&kp SQT"] +
    ["&mt LCTRL CAPS", "&kp Z", "&kp X", "&kp C", "&kp V", "&kp B",
     "&kp N", "&kp M", "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp EQUAL"] +
    ["&kp LGUI", "&kp LALT", "&kp SPACE", "&kp BSPC", "&lt 5 HOME", "&kp PG_UP",
     "&lt 2 DEL", "&lt 4 ENTER", "&mt LALT RALT", "&kp RGUI",
     "&mt LCTRL LBKT", "&lt 6 END", "&kp PG_DN", "&mt RCTRL RBKT"]
)

EMPTY = ["&trans"] * 62

L2 = (
    ["&kp F12", "&kp F1", "&kp F2", "&kp F3", "&kp F4", "&kp F5",
     "&kp F6", "&kp F7", "&kp F8", "&kp F9", "&kp F10", "&kp F11"] +
    ["&trans", "&trans", "&trans", "&trans", "&trans", "&trans",
     "&kp N7", "&kp N7", "&kp N8", "&kp N9", "&trans", "&kp RBKT"] +
    ["&trans", "&to 0", F20, F20, F20, F20,
     "&kp N4", "&kp N4", "&kp N5", "&kp N6", "&kp MINUS", "&kp EQUAL"] +
    ["&trans", F20, F20, F20, F20, F20,
     "&kp N1", "&kp N1", "&kp N2", "&kp N3", "&kp BSLH", "&trans"] +
    ["&trans", "&trans", "&kp SPACE", "&kp BSPC", "&kp HOME", "&kp PG_UP",
     F20, "&kp ENTER", "&trans", "&trans", "&kp LCTRL", "&kp END",
     "&kp PG_DN", "&kp RCTRL"]
)

L4 = (
    ["&kp F12", "&kp F1", "&kp F2", "&kp F3", "&kp F4", "&kp F5",
     "&kp F6", "&kp F7", "&kp F8", "&kp F9", "&kp F10", "&kp F11"] +
    [F20, F20, "&kp LC(W)", "&kp LC(T)", "&kp LC(PG_DN)", "&kp LC(PG_DN)",
     "&kp PG_DN", "&kp HOME", "&kp UP", "&kp INS", "&kp LS(INS)", F20] +
    ["&trans", F20, "&kp LG(LEFT)", "&kp LG(TAB)", "&kp LG(RIGHT)", "&kp LG(RIGHT)",
     "&kp LEFT", "&kp LEFT", "&kp DOWN", "&kp RIGHT", "&kp END", "&kp PSCRN"] +
    ["&trans", F20, F20, F20, "&kp LC(PG_UP)", "&kp LC(PG_UP)",
     "&kp PG_UP", "&trans", "&kp DOWN", F20, "&kp K_APP", "&trans"] +
    ["&trans", "&trans", "&kp SPACE", "&kp BSPC", "&kp HOME", "&kp PG_UP",
     "&kp DEL", F20, "&trans", "&trans", "&kp LCTRL", "&kp END",
     "&kp PG_DN", "&kp RCTRL"]
)

L5 = (
    [F20, F20, F20, F20, F20, "&mo 7", F20, F20, F20, F20, F20, F20] +
    ["&trans", F20, F20, F20, F20, F20,
     F20, F20, "&kp C_VOL_UP", "&kp C_VOL_UP", F20, F20] +
    ["&trans", F20, F20, F20, F20, F20,
     F20, "&kp C_PREV", "&kp C_PP", "&kp C_NEXT", F20, F20] +
    ["&trans", F20, F20, F20, F20, F20,
     F20, "&kp C_MUTE", "&kp C_VOL_DN", "&kp C_VOL_DN", F20, F20] +
    ["&trans", "&trans", "&kp SPACE", "&trans", F20, "&trans",
     "&kp ENTER", "&kp BSPC", "&trans", "&trans", "&kp LCTRL", "&trans",
     "&trans", "&kp RCTRL"]
)

L6 = (
    [F20, F20, F20, F20, F20, "&mo 7", F20, F20, F20, F20, F20, F20] +
    ["&trans", "&none", F20, F20, F20, F20,
     "&msc SCRL_UP", "&msc SCRL_LEFT", "&mmv MOVE_UP", "&msc SCRL_RIGHT", F20, F20] +
    ["&trans", "&none", "&mkp RCLK", "&mkp MCLK", "&mkp LCLK", "&mkp LCLK",
     "&mmv MOVE_LEFT", "&mmv MOVE_LEFT", "&mmv MOVE_DOWN", "&mmv MOVE_RIGHT", F20, F20] +
    ["&trans", "&none", F20, F20, F20, F20,
     "&msc SCRL_DOWN", F20, "&mmv MOVE_DOWN", F20, F20, "&trans"] +
    ["&trans", "&trans", F20, "&kp DEL", "&kp HOME", "&trans",
     "&kp ENTER", "&kp BSPC", "&trans", "&trans", "&trans", "&trans",
     "&trans", "&trans"]
)

L7 = ["&bootloader"] + [F20] * 61

DAC_LAYERS = [L0, EMPTY, L2, EMPTY, L4, L5, L6, L7]
NAMES = ["Base", "L1", "Num", "L3", "Nav", "Media", "Mouse", "Reset"]

for i, lay in enumerate(DAC_LAYERS):
    assert len(lay) == 62, f"layer {i} has {len(lay)} tokens"

# ---- system layer (Adv360-only), defined directly on 76 positions -----
SYS = ["&trans"] * 76
SYS[0] = "&bootloader"; SYS[13] = "&bootloader"
for i, b in enumerate(range(1, 6)):
    SYS[b] = f"&bt BT_SEL {i}"
SYS[8] = "&bt BT_CLR"
SYS[14] = "&studio_unlock"
SYS[15] = "&rgb_ug RGB_TOG"
SYS[16] = "&bl BL_TOG"
for h in HOLES:
    SYS[h] = "&none"


def build_layer(dac):
    out = []
    for adv in range(76):
        if adv in ADV_TO_DAC:
            out.append(dac[ADV_TO_DAC[adv]])
        elif adv in HOLES:
            out.append("&none")
        elif adv in BASE_EXTRA and dac is L0:
            out.append(BASE_EXTRA[adv])
        else:
            out.append("&trans")
    return out


def fmt(tokens):
    # group per physical row: 14 / 14 / 18 / 14 / 16
    rows = [(0, 14), (14, 28), (28, 46), (46, 60), (60, 76)]
    lines = []
    for a, b in rows:
        lines.append("        " + " ".join(tokens[a:b]))
    return "\n".join(lines)


HEADER = '''#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/rgb.h>
#include <dt-bindings/zmk/stp.h>
#include <dt-bindings/zmk/backlight.h>
#include <dt-bindings/zmk/pointing.h>

/ {
    behaviors {
      #include "macros.dtsi"
      #include "version.dtsi"
    };

  keymap {
    compatible = "zmk,keymap";
'''

LAYER_TMPL = '''
    layer_{n} {{
      display-name = "{name}";
      bindings = <
{body}
      >;
    }};
'''

parts = [HEADER]
for n, (dac, name) in enumerate(zip(DAC_LAYERS, NAMES)):
    parts.append(LAYER_TMPL.format(n=n, name=name, body=fmt(build_layer(dac))))
parts.append(LAYER_TMPL.format(n=8, name="Sys", body=fmt(SYS)))
parts.append("  };\n};\n")

open("config/adv360.keymap", "w").write("".join(parts))
print("wrote config/adv360.keymap  (9 layers, 76 keys each)")
