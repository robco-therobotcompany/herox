Based on [ridgeback](https://github.com/ridgeback/ridgeback).

Common packages for HEROX AMR. These packages are relevant for simulation as well as running on the robot hardware.

# OPEN SOURCE LICENSES

For OSS licenses used by dependencies, see [LICENSES.md](LICENSES.md)

# Installation

First, clone the `herox` repository into a catkin workspace:

```bash
ros@ros-usb:~/catkin_ws/src$ git clone git@gitlab.com:kea-robotics/industry_projects/21_amr/herox.git
```

Install the required [fork](https://gitlab.com/kea-robotics/industry_projects/21_amr/ros_canopen) of `ros_canopen` according to the instructions there.

Build the workspace using `catkin_make`:

```bash
ros@ros-usb:~/catkin_ws/src$ cd .. && catkin_make
```

To use the packages, don't forget to source the workspace (using `bash` shell in this example):

```bash
ros@ros-usb:~$ source ~/catkin_ws/devel/setup.bash
```

# Usage

The packages provide different launch files for common tasks and subsystems.

## Control and Teleoperation

To start the low-level motor control software (CAN communication and mecanum controller), use the `control.launch` file of the `herox_control` package. Note, however, that this file is intended to be used by a higher-level launch file. The robot URDF needs to be published first.

To start the motor control software along with a `teleop_twist_joy` node for joystick teleoperation:

```bash
ros@ros-usb:~$ roslaunch herox_control teleop.launch
```

# Configuration

TODO
