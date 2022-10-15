import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[17],
        pins[16],
        pins[15],
        pins[14],
        pins[13],
        pins[12],
    )
    row_pins = (
        pins[7],
        pins[8],
        pins[9],
        pins[10],
        pins[11],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    uart_pin = pins[1]
    rgb_pixel_pin = pins[0]
    data_pin = pins[1]
    i2c = board.I2C

    # flake8: noqa
    # fmt: off
    coord_mapping = [
        0,  1,  2,  3,  4,  5,          35, 34, 33, 32, 31, 30,
        6,  7,  8,  9, 10, 11,          41, 40, 39, 38, 37, 36,
        12, 13, 14, 15, 16, 17,         47, 46, 45, 44, 43, 42,
        18, 19, 20, 21, 22, 23, 29, 59, 53, 52, 51, 50, 49, 48,
                    25, 26, 27, 28, 58, 57, 56, 55,
    ]
