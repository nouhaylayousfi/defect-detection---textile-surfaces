import serial
import time

def send_to_arduino(status):
    ser = serial.Serial("COM3", 9600, timeout=1)
    time.sleep(2)  # attendre Arduino
    ser.write((status + "\n").encode())
    ser.close()
