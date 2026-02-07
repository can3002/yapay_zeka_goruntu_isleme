import serial
import time

ports_to_try = ["COM3","COM4", "COM7", "COM8", "COM9"]  # Bluetooth olan COM'lar

for port in ports_to_try:
    try:
        print(f"Trying {port}...")
        ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(2)  # bağlantı otursun

        # Arduino'ya bir komut gönder
        ser.write(b"1\n")
        print(f"Successfully sent command to {port}")
        ser.close()
        break
    except Exception as e:
        print(f"{port} failed: {e}")
