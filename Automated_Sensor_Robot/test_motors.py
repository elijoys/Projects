# test_motors.py

import time
from motors import MotorController

def main():
    print("Initializing Motor Controller...")
    # Create the controller instance (this automatically activates STBY pin)
    robot = MotorController()
    
    # Define a test speed (approx 60% of max 1023 duty cycle)
    test_speed = 600 
    
    print("Starting motor test sequence in 2 seconds. Lift your robot wheels off the ground!")
    time.sleep(2)

    try:
        while True:
            print("--- Running Forward ---")
            robot.forward(test_speed)
            time.sleep(2)

            print("--- Stopping (Brake) ---")
            robot.stop()
            time.sleep(1)

            print("--- Running Reverse ---")
            robot.reverse(test_speed)
            time.sleep(2)

            print("--- Stopping (Brake) ---")
            robot.stop()
            time.sleep(1)
            
            print("--- Turning Left ---")
            robot.turn_left(test_speed)
            time.sleep(1.5)
            
            print("--- Turning Right ---")
            robot.turn_right(test_speed)
            time.sleep(1.5)
            
            print("--- Stopping (Brake) ---")
            robot.stop()
            time.sleep(3)

    except KeyboardInterrupt:
        # Emergency stop if you press Ctrl+C in Thonny or your terminal
        print("\nTest interrupted by user. Stopping all motors safely...")
        robot.stop()

if __name__ == "__main__":
    main()
