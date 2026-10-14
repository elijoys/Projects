# main.py
# Runs BLE receiver + LED driver + UART debug output

from ble_receiver import BLEReceiver
from led_driver import LEDDriver
import bluetooth
import machine

# =========================
# CONSTANTS
# =========================

LEDS_PER_BLADE = 80
NUM_BLADES = 2
SLICES = 32

BYTES_PER_LED = 3
IMAGE_SIZE = SLICES * LEDS_PER_BLADE * NUM_BLADES * BYTES_PER_LED  # 15360

# =========================
# BUFFERS
# =========================

active_buffer = bytearray(IMAGE_SIZE)
background_buffer = bytearray(IMAGE_SIZE)

display_enabled = True

# =========================
# LED DRIVER (optional test)
# =========================

led = LEDDriver(pin_num=0, total_leds=160)

# =========================
# BUFFER SWAP CALLBACK
# =========================

def on_new_frame():
    global active_buffer, background_buffer

    # swap buffers
    active_buffer, background_buffer = background_buffer, active_buffer

    # DEBUG: send raw data over UART for verification
    uart.write(b"FRAME\n")
    uart.write(active_buffer)

# =========================
# UART (for PC verification)
# =========================

uart = machine.UART(0, baudrate=115200)

# =========================
# BLE SETUP
# =========================

ble = bluetooth.BLE()
receiver = BLEReceiver(ble, background_buffer, on_complete_callback=on_new_frame)

# =========================
# OPTIONAL: SIMPLE LED TEST LOOP
# =========================

slice_index = 0

def tick(timer):
    global slice_index

    offset = slice_index * 480
    led.write(active_buffer[offset:offset + 480])

    slice_index = (slice_index + 1) % 32

timer = machine.Timer()
timer.init(freq=200, mode=machine.Timer.PERIODIC, callback=tick)

print("PICO READY - BLE advertising as 'PICO-POV'")
