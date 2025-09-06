#!/usr/bin/env /usr/bin/python3
import rospy
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3Stamped
import rosbag

class RosbagRecorder:
    def __init__(self):
        rospy.init_node("rosbag_recorder_node")

        # Topics to record
        self.topics = ["/odom", "/imu/accel", "/imu/gyro"]

        # Trigger subscriber
        rospy.Subscriber("/record_trigger", Bool, self.trigger_callback)

        # Bag file
        self.bag = None
        self.recording = False

        # Subscribers for data
        self.subs = []
        rospy.loginfo("Rosbag recorder ready. Send True to /record_trigger to start recording.")

    def trigger_callback(self, msg):
        if msg.data and not self.recording:
            self.start_recording()
        elif not msg.data and self.recording:
            self.stop_recording()

    def start_recording(self):
        filename = rospy.get_param("~bag_filename", "imu_odom.bag")
        self.bag = rosbag.Bag(filename, 'w')
        self.recording = True
        rospy.loginfo(f"Started recording to {filename}")

        # Subscribe to topics
        self.subs = [rospy.Subscriber(t, rospy.AnyMsg, self.callback_wrapper(t)) for t in self.topics]

    def stop_recording(self):
        if self.bag:
            self.bag.close()
        self.recording = False
        rospy.loginfo("Stopped recording.")

        # Unsubscribe
        for sub in self.subs:
            sub.unregister()
        self.subs = []

    def callback_wrapper(self, topic_name):
        def callback(msg):
            if self.recording and self.bag:
                self.bag.write(topic_name, msg)
        return callback

    def spin(self):
        rospy.spin()


if __name__ == "__main__":
    recorder = RosbagRecorder()
    recorder.spin()
