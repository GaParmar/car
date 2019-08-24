## Login Details
 - Username: pi
 - Hostname: car
 - Password: synesthetic

## Default Network Preferences
 - name - "RPI2B_router"
 - password - "password"

## Debug
 - Use terminal over serial
 - Red/Black/White/Green
 - skip red wire if it is already being powered

## ROS architecture overview
 - Catkin Workspace - "/home/pi/ros_catkin_ws"
 - Package - "autonomous_car"

### Camera ROS Node
 - Takes camera images every 0.1 seconds and publishes to /camera_frames

### Motor ROS Node
 - Communicates to the arduino driver through I2C
 - I2C address of the arduino is 0x8
 - Send the updated throttle and steer every 0.1 seconds
 - Throttle message: ['t', <val>]
 - Steer message: ['s', <val>]