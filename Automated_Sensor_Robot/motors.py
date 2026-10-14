# motors.py

from machine import Pin, PWM
import config


class MotorController:

    def __init__(self):
        
        # Set a standard frequency for the PWM pins (e.g., 1000 Hz)
        self.pwm_freq = 1000
        
        # Initialize left motor PWM
        self.left_pwm = PWM(Pin(config.LEFT_PWM_PIN), freq=self.pwm_freq, duty=0)
        
        # Initialize right motor PWM
        self.right_pwm = PWM(Pin(config.RIGHT_PWM_PIN), freq=self.pwm_freq, duty=0)
        
        # Initialize direction pins as OUTPUT
        self.left_in1 = Pin(config.LEFT_IN1_PIN, Pin.OUT)
        self.left_in2 = Pin(config.LEFT_IN2_PIN, Pin.OUT)
        self.right_in1 = Pin(config.RIGHT_IN1_PIN, Pin.OUT)
        self.right_in2 = Pin(config.RIGHT_IN2_PIN, Pin.OUT)
        
        # Initialize STBY and immediately pull it HIGH to enable the driver
        self.motor_standby = Pin(config.STBY_PIN, Pin.OUT)
        self.motor_standby.value(1)


    def _set_speed(self, left_speed, right_speed):
        """Helper function to constrain and set PWM duty cycles (0 to 1023)"""
        # Ensure speed stays within valid 10-bit range (0 - 1023)
        left_speed = max(0, min(1023, left_speed))
        right_speed = max(0, min(1023, right_speed))
        
        self.left_pwm.duty(left_speed)
        self.right_pwm.duty(right_speed)
        


    def forward(self, speed):
        """Moves both motors forward at the given speed (0-1023)"""
        # Left motor forward
        self.left_in1.value(1)
        self.left_in2.value(0)
        
        # Right motor forward
        self.right_in1.value(1)
        self.right_in2.value(0)
        
        self._set_speed(speed, speed)
        


    def reverse(self, speed):
        """Moves both motors backward at the given speed (0-1023)"""
        # Left motor reverse
        self.left_in1.value(0)
        self.left_in2.value(1)
        
        # Right motor reverse
        self.right_in1.value(0)
        self.right_in2.value(1)
        
        self._set_speed(speed, speed)
        


    def stop(self):
        """Stops both motors immediately by pulling PWM to 0 and braking"""
        self._set_speed(0, 0)
        
        # Short brake mode (IN1 and IN2 both HIGH)
        self.left_in1.value(1)
        self.left_in2.value(1)
        self.right_in1.value(1)
        self.right_in2.value(1)
        


    def turn_left(self, speed):
        """Turns left on the spot by reversing left and driving right forward"""
        # Left motor reverse
        self.left_in1.value(0)
        self.left_in2.value(1)
        
        # Right motor forward
        self.right_in1.value(1)
        self.right_in2.value(0)
        
        self._set_speed(speed, speed)



    def turn_right(self, speed):
        """Turns right on the spot by driving left forward and reversing right"""
        # Left motor forward
        self.left_in1.value(1)
        self.left_in2.value(0)
        
        # Right motor reverse
        self.right_in1.value(0)
        self.right_in2.value(1)
        
        self._set_speed(speed, speed)