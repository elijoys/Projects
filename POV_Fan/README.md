# TailSpin
Sub $100 holographic fan that allows you to upload and display any image you want via a custom web application HMI 
Nordic UART streams data packages via BLE to rotating hub controller

# Hardware + Software Overview
<ins>Hardware</ins>
- 2x PicoW microcontrollers
- Custom PCB blades
- 24 BLDC Motor
- Fully 3D-printed chassis
- Slip ring
- DC Power Supply

<ins>Software</ins>
- HTML / Javascript - HMI
- Python - motor driver, BLE, LED driver, LED timing

# Folders + File Overview
<ins>ControllerA</ins>
- Only responsible for controlling the motor via PID
- file
    - FinalMotorDriver.py
  
<ins>ControllerB / HMI</ins>
- Facilitates bluetooth connection and image slicing
- files
    - main.py
    - ble_advertising.py
    - ble_receiver.py
    - config.py
    - display_controller.py
    - led_driver.py
    - hmi.html

