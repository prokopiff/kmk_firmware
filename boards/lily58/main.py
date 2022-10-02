from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.hid import HIDModes
from kmk.handlers.sequences import send_string
import supervisor
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.sticky_mod import StickyMod
import storage

TAP_TIME = 250

keyboard = KMKKeyboard()
layers = Layers()
layers.tap_time = TAP_TIME
keyboard.modules.append(layers)
mod_tap = ModTap()
mod_tap.tap_time = TAP_TIME
keyboard.modules.append(mod_tap)
keyboard.modules.append(StickyMod())
keyboard.extensions.append(MediaKeys())

# oled
# oled_ext = Oled(OledData(corner_one={0:OledReactionType.STATIC,1:["1 2 3 4 5 6","","","","","","",""]},corner_two={0:OledReactionType.STATIC,1:[" 7 8 Layer","","","","","",""," 7 8 Layer"]},corner_three={0:OledReactionType.LAYER,1:["^","  ^","    ^","      ^","        ^","          ^","",""]},corner_four={0:OledReactionType.LAYER,1:["","","","","",""," ^","   ^"]}),toDisplay=OledDisplayMode.TXT,flip= True)
# keyboard.extensions.append(oled_ext)

if storage.getmount("/").label[-1] == "L":
    split_side = SplitSide.LEFT
else:
    split_side = SplitSide.RIGHT
split = Split(split_side = split_side,use_pio=True)
keyboard.modules.append(split)

# Custom keycodes
BSP_LWR = KC.LT(1, KC.BSPC, prefer_hold=True)
BSP_ADJ = KC.LT(3, KC.BSPC, prefer_hold=True)
DEL_LWR = KC.LT(1, KC.DEL, prefer_hold=True)
SPC_LSFT = KC.MT(KC.SPC, KC.LSFT, prefer_hold=True)
SPC_RSFT = KC.MT(KC.SPC, KC.RSFT, prefer_hold=True)
ENT_RSE = KC.LT(2, KC.ENT, prefer_hold=True)
ENT_ADJ = KC.LT(3, KC.ENT, prefer_hold=True)

keyboard.keymap = [
    [ # 0 Main
        KC.ESCAPE, KC.N1, KC.N2, KC.N3,   KC.N4,    KC.N5,                                     KC.N6,    KC.N7,   KC.N8,    KC.N9,  KC.N0,     KC.GRAVE,
        KC.TAB,    KC.Q,  KC.W,  KC.E,    KC.R,     KC.T,                                      KC.Y,     KC.U,    KC.I,     KC.O,   KC.P,      KC.LBRC,
        KC.LCTRL,  KC.A,  KC.S,  KC.D,    KC.F,     KC.G,                                      KC.H,     KC.J,    KC.K,     KC.L,   KC.SCOLON, KC.QUOTE,
        KC.LALT,   KC.Z,  KC.X,  KC.C,    KC.V,     KC.B,     KC.KP_MINUS,        KC.KP_PLUS,  KC.N,     KC.M,    KC.COMMA, KC.DOT, KC.SLASH,  KC.RBRC,
                                 KC.LGUI, BSP_LWR,  SPC_LSFT, ENT_RSE,            ENT_RSE,     SPC_RSFT, DEL_LWR, KC.SM(KC.TAB, KC.LCTRL),
    ],
    [ # 1 Lower
        KC.F1,     KC.F2,      KC.F3,   KC.F4,   KC.F5,   KC.F6,                           KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,
        KC.TRNS,   KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS,   KC.EXCLAIM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                         KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.UNDS,
        KC.TRNS,   KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.MPRV,       KC.MNXT, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                        KC.TRNS, KC.TRNS, KC.TRNS, ENT_ADJ,       ENT_ADJ, KC.TRNS, KC.TRNS, KC.SM(KC.TAB, KC.LALT),
    ],
    [ # 2 Raise
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TG(4),
        KC.TRNS, KC.PAST, KC.P7,   KC.P8,   KC.P9,   KC.PMNS,                         KC.EQL, KC.HOME, KC.UP,   KC.PGUP, KC.TRNS,  KC.TRNS,
        KC.TRNS, KC.PSLS, KC.P4,   KC.P5,   KC.P6,   KC.PPLS,                         KC.TRNS, KC.LEFT, KC.DOWN, KC.RGHT, KC.TRNS, KC.TRNS,
        KC.NLCK, KC.P0,   KC.P1,   KC.P2,   KC.P3,   KC.PDOT, KC.VOLD,       KC.VOLU, KC.TRNS, KC.END,  KC.PSCR, KC.PGDN, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.ENT,        KC.ENT, KC.TRNS, KC.TRNS, KC.SM(KC.TAB, KC.LALT),
    ],
    [ # 3 Adjust
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [ # 4 Game
        KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.LSFT,  KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.LCTRL, KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.H,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                    KC.MO(5), KC.BSPC, KC.SPC,  KC.ENT,        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [ # 5 Game 2
        KC.TRNS, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                           KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F12,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
]

# keyboard.debug_enabled = True

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
