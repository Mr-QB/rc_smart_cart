#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import serial

def main():
    rospy.init_node('ai_predict_listener')

    port = rospy.get_param('~port', '/dev/ttyACM0')
    baud = rospy.get_param('~baudrate', 115200)

    # Publisher
    pub = rospy.Publisher('/ai_predict', String, queue_size=50)

    try:
        ser = serial.Serial(port, baud, timeout=0.01)
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
                line = line.strip()
                if line.startswith("AI_PREDICT"):
                    parts = line.split()
                    if len(parts) != 4:
                        continue

                    prob_normal = parts[1]
                    prob_not_normal = parts[2]
                    label_final = parts[3]

                    msg = f"{prob_normal} {prob_not_normal} {label_final}"
                    pub.publish(msg)

        rate.sleep()

    ser.close()

if __name__ == "__main__":
    main()
