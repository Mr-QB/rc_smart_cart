#!/usr/bin/env python3
import rosbag
import csv

bag_file = "catkin_ws/suc_data_bag.bag"
out_file = "training_data_2.csv"

accel_msgs, gyro_msgs, odom_msgs = [], [], []

with rosbag.Bag(bag_file) as bag:
    start_time = bag.get_start_time()
    end_time   = bag.get_end_time()

    # Cắt 3s đầu và 3s cuối
    trim_start = start_time + 3.0
    trim_end   = end_time - 3.0

    for topic, msg, t in bag.read_messages(topics=["/imu/accel", "/imu/gyro", "/odom"]):
        ts = t.to_sec()
        if ts < trim_start or ts > trim_end:
            continue  # bỏ ngoài vùng quan tâm

        if topic == "/imu/accel":
            accel_msgs.append((ts, msg.vector.x, msg.vector.y, msg.vector.z))
        elif topic == "/imu/gyro":
            gyro_msgs.append((ts, msg.vector.x, msg.vector.y, msg.vector.z))
        elif topic == "/odom":
            odom_msgs.append((
                ts,
                msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z,
                msg.twist.twist.angular.x, msg.twist.twist.angular.y, msg.twist.twist.angular.z
            ))

def find_nearest(msgs, t):
    return min(msgs, key=lambda x: abs(x[0] - t)) if msgs else [t] + [0.0]*(len(msgs[0])-1)

with open(out_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "time",
        "accel_x", "accel_y", "accel_z",
        "gyro_x", "gyro_y", "gyro_z",
        "odom_lin_x", "odom_lin_y", "odom_lin_z",
        "odom_ang_x", "odom_ang_y", "odom_ang_z"
    ])

    for t, ax, ay, az in accel_msgs:
        gx, gy, gz = find_nearest(gyro_msgs, t)[1:]
        od = find_nearest(odom_msgs, t)
        writer.writerow([
            t,
            ax, ay, az,
            gx, gy, gz,
            od[1], od[2], od[3], od[4], od[5], od[6]
        ])

print(f"✅ Đã lưu dữ liệu (bỏ 3s đầu/cuối) vào {out_file}")
