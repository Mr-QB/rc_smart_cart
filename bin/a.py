import serial, struct, time

ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=0.01)
time.sleep(2)

try:
    while True:
        v_left = -0.4
        v_right = 0.34

        # sử dụng big-endian để MCU đọc đúng
        data = struct.pack("<ff", v_left, v_right)  # '>' = big-endian
        print("Hex:", data.hex())

        # gửi sync byte + 8 byte dữ liệu
        ser.write(b"\xaa" + data)

        print(f"Sent: v_left={v_left}, v_right={v_right}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")
finally:
    ser.close()
    
