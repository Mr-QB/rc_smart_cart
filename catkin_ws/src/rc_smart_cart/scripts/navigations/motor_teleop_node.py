#!/usr/bin/env /usr/bin/python3 
# import rospy
from std_msgs.msg import Float32MultiArray
import sys
import termios
import tty
import rospy

STEP_V = 0.05  # m/s
STEP_W = 0.05  # rad/s

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def teleop_node():
    rospy.init_node("motor_teleop_node")
    pub = rospy.Publisher("cmd_vel_motor", Float32MultiArray, queue_size=1)
    rospy.loginfo("Teleop node started. Use WASD to move, Q/E to rotate, X to stop.")

    v_left = 0.0
    v_right = 0.0

    while not rospy.is_shutdown():
        key = getch()
        if key.lower() == 'w':      
            v_left += STEP_V
            v_right += STEP_V
        elif key.lower() == 's':     
            v_left -= STEP_V
            v_right -= STEP_V
        elif key.lower() == 'a':     
            v_left -= STEP_W
            v_right += STEP_W
        elif key.lower() == 'd':    
            v_left += STEP_W
            v_right -= STEP_W
        elif key.lower() == 'x':    
            v_left = 0.0
            v_right = 0.0
        elif key.lower() == 'q':     
            break

        v_left = max(min(v_left, 0.64), -0.64)
        v_right = max(min(v_right, 0.64), -0.64)

        msg = Float32MultiArray()
        msg.data = [v_left, v_right]
        pub.publish(msg)
        rospy.loginfo(f"v_left={v_left:.2f}, v_right={v_right:.2f}")

    msg = Float32MultiArray()
    msg.data = [0.0, 0.0]
    pub.publish(msg)
    rospy.loginfo("Teleop stopped, motors set to 0.")

if __name__ == "__main__":
    try:
        teleop_node()
    except rospy.ROSInterruptException:
        pass
