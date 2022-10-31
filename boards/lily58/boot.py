import digitalio
import storage
import usb_cdc
import usb_hid

from kb import KMKKeyboard
from kmk.scanners import DiodeOrientation


# If this key is held during boot, don't run the code which hides the storage and disables serial
# This will use the first row/col pin. Feel free to change it if you want it to be another pin
col = digitalio.DigitalInOut(KMKKeyboard.col_pins[0])
row = digitalio.DigitalInOut(KMKKeyboard.row_pins[0])

if KMKKeyboard.diode_orientation == DiodeOrientation.COLUMNS:
  col.switch_to_output(value=True)
  row.switch_to_input(pull=digitalio.Pull.DOWN)
else:
  col.switch_to_input(pull=digitalio.Pull.DOWN)
  row.switch_to_output(value=True)

if not row.value:
  storage.disable_usb_drive()
  # Equivalent to usb_cdc.enable(console=False, data=False)
  usb_cdc.disable()
  usb_hid.enable(boot_device=1)
else:
  storage.remount("/", readonly=False)
  m = storage.getmount("/")
  m.label = "LILY58L"
  storage.remount("/", readonly=True)
  storage.enable_usb_drive()

row.deinit()
col.deinit()
