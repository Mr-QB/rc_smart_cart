#!/usr/bin/env python3
import rosbag
import csv
import os

files = {
    "catkin_ws/data_bag_true.bag":  "training_data_true.csv",
    "catkin_ws/data_bag_false.bag": "training_data_false.csv"
}

def bag_to_csv(bag_file, out_file):
    accel_msgs, gyro_msgs, odom_msgs = [], [], []

    with rosbag.Bag(bag_file) as bag:
        start_time = bag.get_start_time()
        end_time   = bag.get_end_time()

        trim_start = start_time + 3.0
        trim_end   = end_time - 3.0

        for topic, msg, t in bag.read_messages(topics=["/imu/accel", "/imu/gyro", "/odom"]):
            ts = t.to_sec()
            if ts < trim_start or ts > trim_end:
                continue 

            if topic == "/imu/accel":
                accel_msgs.append((ts, msg.vector.x, msg.vector.y, msg.vector.z))
            elif topic == "/imu/gyro":
                gyro_msgs.append((ts, msg.vector.x, msg.vector.y, msg.vector.z))
            elif topic == "/odom":
                # Chỉ lấy linear.x (v) và angular.z (w)
                odom_msgs.append((ts, msg.twist.twist.linear.x, msg.twist.twist.angular.z))

    def find_nearest(msgs, t):
        return min(msgs, key=lambda x: abs(x[0] - t)) if msgs else [t] + [0.0]*(len(msgs[0])-1)

    with open(out_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "time",
            "accel_x", "accel_y", "accel_z",
            "gyro_x", "gyro_y", "gyro_z",
            "odom_lin_x",  # v
            "odom_ang_z"   # w
        ])

        for t, ax, ay, az in accel_msgs:
            gx, gy, gz = find_nearest(gyro_msgs, t)[1:]
            od = find_nearest(odom_msgs, t)
            writer.writerow([
                t,
                ax, ay, az,
                gx, gy, gz,
                od[1], od[2]
            ])

for bag_file, out_file in files.items():
    print(f"Processing {bag_file} -> {out_file}")
    bag_to_csv(bag_file, out_file)
    print(f"Done: {out_file}")
