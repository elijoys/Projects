# TailSpin
Sub $100 holographic fan that allows you to upload and display any image you want via a custom web application HMI 
Nordic UART streams data packages via BLE to rotating hub controller

# Hardware + Software Overview
Hardware
- 2x PicoW microcontrollers
- Custom PCB blades
- 24 BLDC Motor
- Fully 3D-printed chassis
- Slip ring
- DC Power Supply

Software 
- HTML / Javascript - HMI
- Python - motor driver, BLE, LED driver, LED timing

# Folders + File Overview
ControllerA
- Only responsible for controlling the motor via PID
- file
    - FinalMotorDriver.py
  
ControllerB / HMI 
- Facilitates bluetooth connection and image slicing
- files
    - main.py
    - ble_advertising.py
    - ble_receiver.py
    - config.py
    - display_controller.py
    - led_driver.py
    - hmi.html

