# LiDAR-Based Object Detection using ROS2

## Overview
This project implements a real-time LiDAR-based perception system using ROS2.  
It processes raw LiDAR data to detect objects, track them over time, estimate distance and velocity, and classify them into safety zones.

The system is simulated using Gazebo and visualized in RViz.

---

## Features
- Object detection using clustering
- Object tracking with unique IDs
- Distance estimation from robot
- Velocity estimation (relative motion)
- Zone classification:
  - DANGER
  - WARNING
  - SAFE
- Real-time visualization in RViz
- Teleoperation support

---

## System Pipeline
LiDAR Scan → Cartesian Conversion → Clustering → Tracking → Zone Classification → Visualization

---

## Tech Stack
- ROS2 (Jazzy)
- Python
- Gazebo
- RViz
- NumPy

---

## Project Structure
lidar_detection/
- clustering.py
- tracking.py
- zones.py
- scan_processor.py
- __init__.py

---

## Installation

Clone the repository:
git clone https://github.com/PES2UG23CS320/lidar-object-detection.git

Build the package:
cd ~/ros2_ws
colcon build --packages-select lidar_detection
source install/setup.bash

---

## Running the Project

Launch Gazebo:
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py

Run detection node:
source ~/ros2_ws/install/setup.bash
ros2 run lidar_detection scan_processor

Open RViz:
rviz2

In RViz:
- Fixed Frame → base_link
- Add → LaserScan (/scan)
- Add → Marker (/visualization_marker)

Run teleop:
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard

---

## Results
- Objects detected as clusters
- Unique IDs assigned and tracked
- Distance calculated in real time
- Zone classification:
  - DANGER (< 0.5 m)
  - WARNING (< 1.5 m)
  - SAFE (> 1.5 m)
- Visualization with markers and labels in RViz

---

## Example Output
ID 1 | Dist: 0.91 | Vel: 0.00 | Zone: WARNING  
ID 2 | Dist: 1.70 | Vel: 0.01 | Zone: SAFE  

---

## Known Issues
- Gazebo may show missing mesh warnings (visual only)
- Velocity is relative to robot motion
- Minor noise in clustering

---

## Future Improvements
- Use global frame for accurate velocity
- Add moving objects in simulation
- Improve clustering algorithm
- Add obstacle avoidance

