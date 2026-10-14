# test_ultrasonic.py

from ultrasonic import UltrasonicSensor
import time

# Create ultrasonic sensor object
sensor = UltrasonicSensor()

print("Ultrasonic sensor test starting...")
print("Place an object in front of the sensor.")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        distance = sensor.measure_distance_cm()

        if distance is None:
            print("No valid reading")
        else:
            print("Distance: {:.2f} cm".format(distance))

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nUltrasonic test stopped.")