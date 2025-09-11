#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean(csv_file):
    df = pd.read_csv(csv_file)
    df["time"] = df["time"] - df["time"].iloc[0]
    # df = df[~(((df["time"] >= 40) & (df["time"] <= 51)) |
    #           ((df["time"] >= 58) & (df["time"] <= 68)))]
    return df

def plot_dataset(df, title_prefix):
    plt.figure(figsize=(12, 8))

    # --- Accel ---
    plt.subplot(3, 1, 1)
    plt.plot(df["time"], df["accel_x"], label="accel_x")
    plt.plot(df["time"], df["accel_y"], label="accel_y")
    plt.plot(df["time"], df["accel_z"], label="accel_z")
    plt.legend()
    plt.title(f"{title_prefix} - IMU Acceleration")
    plt.xlabel("time [s]")
    plt.ylabel("m/s^2")

    # --- Gyro ---
    plt.subplot(3, 1, 2)
    plt.plot(df["time"], df["gyro_x"], label="gyro_x")
    plt.plot(df["time"], df["gyro_y"], label="gyro_y")
    plt.plot(df["time"], df["gyro_z"], label="gyro_z")
    plt.legend()
    plt.title(f"{title_prefix} - IMU Gyroscope")
    plt.xlabel("time [s]")
    plt.ylabel("rad/s")

    # --- Odom Twist (lin_x & ang_z) ---
    plt.subplot(3, 1, 3)
    plt.plot(df["time"], df["odom_lin_x"], label="lin_x")
    plt.plot(df["time"], df["odom_ang_z"], label="ang_z")
    plt.legend()
    plt.title(f"{title_prefix} - Odometry Twist")
    plt.xlabel("time [s]")
    plt.ylabel("velocity")

    plt.tight_layout()

# Load 2 dataset
df_true  = load_and_clean("training_data_true.csv")
df_false = load_and_clean("training_data_false.csv")

plot_dataset(df_true, "TRUE Dataset")
plot_dataset(df_false, "FALSE Dataset")

plt.show()
