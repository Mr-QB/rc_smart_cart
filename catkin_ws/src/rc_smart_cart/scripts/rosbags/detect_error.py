#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

df_true  = pd.read_csv("training_data_true.csv")
df_false = pd.read_csv("training_data_false.csv")

features = ["accel_x","accel_y","accel_z",
            "gyro_x","gyro_y","gyro_z",
            "odom_lin_x","odom_ang_z"]

df_true  = df_true[features]
df_false = df_false[features]

df_true["label"]  = 1
df_false["label"] = 0

def create_sequences(df, seq_len=4):
    X, y = [], []
    data = df.values
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len, :-1])
        y.append(data[i+seq_len-1, -1])
    return np.array(X), np.array(y)

X_true, y_true   = create_sequences(df_true, seq_len=4)
X_false, y_false = create_sequences(df_false, seq_len=4)

print(X_true.shape, y_true.shape)
print(X_false.shape, y_false.shape)

X = np.concatenate([X_true, X_false], axis=0)
y = np.concatenate([y_true, y_false], axis=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4, 8)),
    tf.keras.layers.Flatten(),          # flatten 4x8 -> 32
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

# Train
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=45, batch_size=32)


converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = []  
tflite_model = converter.convert()

# 5. Lưu file
with open("model_float.tflite", "wb") as f:
    f.write(tflite_model)

print("Đã tạo file model_float.tflite thành công!")
