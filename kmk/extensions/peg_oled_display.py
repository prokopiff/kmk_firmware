try:
    from typing import Callable, Optional, Tuple
except ImportError:
    pass

import busio
import gc

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key

from kmk.utils import Debug

debug = Debug(__name__)

class OledDisplayMode:
    TXT = 0
    IMG = 1


class OledReactionType:
    STATIC = 0
    LAYER = 1


class OledData:
    def __init__(
        self,
        image=None,
        corner_one=None,
        corner_two=None,
        corner_three=None,
        corner_four=None,
    ):
        if image:
            self.data = [image]
        elif corner_one and corner_two and corner_three and corner_four:
            self.data = [corner_one, corner_two, corner_three, corner_four]


class Oled(Extension):
    def __init__(
        self,
        views,
        toDisplay=OledDisplayMode.TXT,
        oWidth=128,
        oHeight=32,
        flip: bool = False,
        sleep_timeout: int = 0,
        set_timeout: Callable[[int, Callable[[None], None]], Tuple[int, int]] = None,
        cancel_timeout: Callable[[Tuple[int, int]], None] = None,
    ):
        displayio.release_displays()
        self.rotation = 180 if flip else 0
        self._views = views.data
        self._toDisplay = toDisplay
        self._width = oWidth
        self._height = oHeight
        self._prevLayers = 0
        self._sleep_timeout = sleep_timeout
        self._set_timeout = set_timeout
        self._cancel_timeout = cancel_timeout
        self._timer: Tuple[int, int] = (-1, -1)
        self._brightness_step = 0.1

        make_key(
            names=("OLED_BRI",), on_press=self._oled_bri, on_release=handler_passthrough
        )
        make_key(
            names=("OLED_BRD",), on_press=self._oled_brd, on_release=handler_passthrough
        )

        gc.collect()

    def returnCurrectRenderText(self, layer, singleView):
        # for now we only have static things and react to layers. But when we react to battery % and wpm we can handle the logic here
        if singleView[0] == OledReactionType.STATIC:
            return singleView[1][0]
        if singleView[0] == OledReactionType.LAYER:
            return singleView[1][layer]

    def renderOledTextLayer(self, layer):
        splash = displayio.Group()
        splash.append(
            label.Label(
                terminalio.FONT,
                text=self.returnCurrectRenderText(layer, self._views[0]),
                color=0xFFFFFF,
                x=0,
                y=10,
            )
        )
        splash.append(
            label.Label(
                terminalio.FONT,
                text=self.returnCurrectRenderText(layer, self._views[1]),
                color=0xFFFFFF,
                x=64,
                y=10,
            )
        )
        splash.append(
            label.Label(
                terminalio.FONT,
                text=self.returnCurrectRenderText(layer, self._views[2]),
                color=0xFFFFFF,
                x=0,
                y=25,
            )
        )
        splash.append(
            label.Label(
                terminalio.FONT,
                text=self.returnCurrectRenderText(layer, self._views[3]),
                color=0xFFFFFF,
                x=64,
                y=25,
            )
        )
        self._display.show(splash)
        gc.collect()

    def renderOledImgLayer(self, layer):
        splash = displayio.Group()
        odb = displayio.OnDiskBitmap(
            '/' + self.returnCurrectRenderText(layer, self._views[0])
        )
        image = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        splash.append(image)
        self._display.show(splash)
        gc.collect()

    def updateOLED(self, sandbox):
        if self._toDisplay == OledDisplayMode.TXT:
            self.renderOledTextLayer(sandbox.active_layers[0])
        if self._toDisplay == OledDisplayMode.IMG:
            self.renderOledImgLayer(sandbox.active_layers[0])
        gc.collect()

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        displayio.release_displays()
        i2c = busio.I2C(keyboard.SCL, keyboard.SDA)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=0x3C),
            width=self._width,
            height=self._height,
            rotation=self.rotation,
            brightness=0.1,
        )
        if self._toDisplay == OledDisplayMode.TXT:
            self.renderOledTextLayer(0)
        if self._toDisplay == OledDisplayMode.IMG:
            self.renderOledImgLayer(0)

        self._timer = self._set_timeout(self._sleep_timeout, self._sleep)


    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)

    def after_matrix_scan(self, sandbox):
        if not sandbox.matrix_update:
            return

        if not self._sleep_timeout:
            return

        if not self._display.is_awake:
            self._display.wake()

        self._cancel_timeout(self._timer)
        self._timer = self._set_timeout(self._sleep_timeout, self._sleep)

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def _sleep(self):
        self._display.sleep()

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return


    def _oled_bri(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness + self._brightness_step
            if self._display.brightness + self._brightness_step <= 1.0
            else 1.0
        )
        self._brightness = self._display.brightness  # Save current brightness
        self._display.refresh()
        debug(f"New br: {self._display.brightness}")

    def _oled_brd(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness - self._brightness_step
            if self._display.brightness - self._brightness_step >= 0.1
            else 0.1
        )
        self._brightness = self._display.brightness
        self._display.refresh()
        debug(f"New br: {self._display.brightness}")
