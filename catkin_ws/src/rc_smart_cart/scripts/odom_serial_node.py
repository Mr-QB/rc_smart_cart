#!/usr/bin/env /usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3Stamped
from tf.transformations import quaternion_from_euler
import serial

def split_line(line):
    return line.strip().split()

def main():
    rospy.init_node('odom_serial')

    port = rospy.get_param('~port', '/dev/ttyACM0')
    baud = rospy.get_param('~baudrate', 9600)

    # Publishers
    odom_pub = rospy.Publisher('/odom', Odometry, queue_size=50)
    accel_pub = rospy.Publisher('/imu/accel', Vector3Stamped, queue_size=50)
    gyro_pub  = rospy.Publisher('/imu/gyro', Vector3Stamped, queue_size=50)

    try:
        ser = serial.Serial(port, baud, timeout=0.01)
        rospy.loginfo(f"Opened serial port {port} at {baud} baud")
    except serial.SerialException as e:
        rospy.logerr(f"Cannot open serial port: {e}")
        return

    line_buf = ""
    rate = rospy.Rate(50)  # 50 Hz

    while not rospy.is_shutdown():
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            line_buf += data

            while '\n' in line_buf:
                line, line_buf = line_buf.split('\n', 1)
                parts = split_line(line)
                if len(parts) != 15 or parts[0] != "ODOM":
                    continue  # không đúng định dạng thì bỏ

                try:
                    # ODOM
                    x = float(parts[1])
                    y = float(parts[2])
                    theta = float(parts[3])
                    v = float(parts[5])
                    w = float(parts[6])

                    # IMU
                    accel = [float(parts[9]), float(parts[10]), float(parts[11])]
                    gyro  = [float(parts[12]), float(parts[13]), float(parts[14])]
                except ValueError:
                    continue  # lỗi convert float bỏ dòng

                # Publish Odometry
                odom_msg = Odometry()
                odom_msg.header.stamp = rospy.Time.now()
                odom_msg.header.frame_id = "odom"
                odom_msg.child_frame_id = "base_link"
                odom_msg.pose.pose.position.x = x
                odom_msg.pose.pose.position.y = y
                odom_msg.pose.pose.position.z = 0.0
                q = quaternion_from_euler(0, 0, theta)
                odom_msg.pose.pose.orientation.x = q[0]
                odom_msg.pose.pose.orientation.y = q[1]
                odom_msg.pose.pose.orientation.z = q[2]
                odom_msg.pose.pose.orientation.w = q[3]
                odom_msg.twist.twist.linear.x = v
                odom_msg.twist.twist.angular.z = w
                odom_pub.publish(odom_msg)

                # Publish Accel
                accel_msg = Vector3Stamped()
                accel_msg.header.stamp = rospy.Time.now()
                accel_msg.vector.x = accel[0]
                accel_msg.vector.y = accel[1]
                accel_msg.vector.z = accel[2]
                accel_pub.publish(accel_msg)

                # Publish Gyro
                gyro_msg = Vector3Stamped()
                gyro_msg.header.stamp = rospy.Time.now()
                gyro_msg.vector.x = gyro[0]
                gyro_msg.vector.y = gyro[1]
                gyro_msg.vector.z = gyro[2]
                gyro_pub.publish(gyro_msg)

        rate.sleep()

    ser.close()

if __name__ == "__main__":
    main()
