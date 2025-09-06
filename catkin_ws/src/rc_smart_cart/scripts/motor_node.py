#!/usr/bin/env /usr/bin/python3 
import rospy
from std_msgs.msg import Float32MultiArray
import serial
import struct
import time
import sys


class MotorController:
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=0.01)
            rospy.loginfo(f"Serial connected on {port} at {baudrate} baud.")
            time.sleep(2)  # allow MCU to reset
        except serial.SerialException as e:
            rospy.logerr(f"Cannot open serial port: {e}")
            sys.exit(1)

        # Subscribe to cmd_vel_motor topic
        rospy.Subscriber("cmd_vel_motor", Float32MultiArray, self.callback)
        rospy.on_shutdown(self.cleanup)
        rospy.loginfo("Motor controller node started...")

    def callback(self, msg):
        if len(msg.data) != 2:
            rospy.logwarn("Expected 2 float values: [v_left, v_right]")
            return
        v_left, v_right = msg.data
        v_left = max(min(v_left, 0.64), -0.64)
        v_right = max(min(v_right, 0.64), -0.64)

        # Pack floats in little-endian for MCU
        data = struct.pack("<ff", v_left, v_right)
        self.ser.write(b"\xaa" + data)
        rospy.loginfo(f"Sent velocities -> v_left: {v_left}, v_right: {v_right}")

    def cleanup(self):
        # Stop motors when shutting down
        try:
            self.ser.write(b"\xaa" + struct.pack("<ff", 0.0, 0.0))
            self.ser.close()
            rospy.loginfo("Serial closed, motors stopped.")
        except Exception as e:
            rospy.logwarn(f"Error closing serial: {e}")


if __name__ == "__main__":
    rospy.init_node("motor_controller_node")
    port = rospy.get_param("~port", "/dev/ttyUSB0")
    baudrate = rospy.get_param("~baudrate", 115200)
    controller = MotorController(port=port, baudrate=baudrate)
    rospy.spin()
