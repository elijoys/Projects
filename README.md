# Projects
Complete collection of all academic + personal project code

Below is a list of all projects and their summary.

# Senior Capstone: POV Holographic Fan Display ⚡️
- Sub $100 holographic fan that allows you to upload and display any image you want via a custom web application HMI 
- Nordic UART streams data packages via BLE to rotating hub controller

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

----------------------------------------------------------------------------------------------------
# Bioinstrumentation Course: ACL Injury Recovery System 🦵
Device that senses and quantifies hamstring asymmetry, identifies injury risk, provides real-time feedback, and tracks progress over time. 
Records surface EMG from both hamstrings, converts data to estimated torque, and computes limb symmetry index (LSI) for meaningful feedback. 

Hardware:
- Surface EMG electrodes
- Dual-channel EMG amplifier & filter circuits
- Arduino Due microcontroller
- 16x2 LCD
- DC power supply 

Software 
- Simplified C++ (Arduino IDE)

----------------------------------------------------------------------------------------------------
# AI in Computing and Robotics Research: Project 1: Cocktail Recommender 🍸🍹
Recommends the 5 best cocktails (output) based on ingredients you have at home (input), as well as directions for making your favorite. 

Unsupervised ML model 
- Uses TF-IDF, Cosine Similarity, and Clustering 
- Python

----------------------------------------------------------------------------------------------------
# AI in Computing and Robotics Research: Project 2: Wildfire Detection from Image Data 🌳📸
Analyzes aerial images of forested areas (both inflamed and non-inflamed) and determines whether or not there is a wildfire. 

Supervised image classification ML model 
- FLAME 2 Dataset
- Python

----------------------------------------------------------------------------------------------------
# AI in Computing and Robotics Research: Project 3: 3D Digital Twin Robotic Object Interaction 🤖🚘
Trained a virtual car to navigate obstacles and avoid walls, uses its own sensor data and sensor data from a drone flying overhead. 
Reinforcement learning
- Unity environment, ML-Agents
- C++

----------------------------------------------------------------------------------------------------
# Microcontroller Project: Reaction Timer ⏰
Reaction timer that counts up on a seven-segment display, then stops counting once a button is pressed. 
Ful life cycle embedded project - requirements, implementation, debugging, demo. 
- PPS peripheral mapping, seven-segment display driver, 4 bit counter with decoder, 4 to 16 bit decoder
- PIC32

----------------------------------------------------------------------------------------------------
# In progress: Automated Sensor Robot 🤖🛞⏳
Autonomous mobile robot that can:
- Sense its environment
- Detect obstacles
- Make navigation decisions 
- Drive autonomously 
Hardware
- ESP32
- 2xTT geared DC motors
- TB6612FNG dual motor driver
- HC-SR04 ultrasonic sensor 
- SG90 servo
- 4xAA battery pack
- Wheels

Software
- Python -> measure distance, sweep sensor, understand local environment, choose desired action, manage robot behavior/state, control physical motors, safety override, coordinate all systems 
