# ultrasonic.py

from machine import Pin, time_pulse_us
import config
import time


class UltrasonicSensor:
    def __init__(self):

        # Initialize trigger and echo pins
        self.trigger_pin = Pin(
            config.ULTRASONIC_TRIGGER_PIN,
            Pin.OUT
        )

        self.echo_pin = Pin(
            config.ULTRASONIC_ECHO_PIN,
            Pin.IN
        )

        # Make sure trigger starts LOW
        self.trigger_pin.value(0)

    def measure_distance_cm(self):

        # Send 10 us trigger pulse
        self.trigger_pin.value(0)
        time.sleep_us(2)

        self.trigger_pin.value(1)
        time.sleep_us(10)

        self.trigger_pin.value(0)

        # Measure how long Echo stays HIGH
        duration = time_pulse_us(
            self.echo_pin,
            1,
            30000
        )

        # Check for timeout/error
        if duration < 0:
            print("Ultrasonic timing failed")
            return None

        # Convert microseconds to centimeters
        distance = (duration * 0.0343) / 2

        return distance