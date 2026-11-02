import serial
import time
import struct

PAYLOAD_SIZE = 17 
START_MARKER = b'\xfa\xfa'
END_MARKER = b'\xAF\xAF\xAF'
SERIAL_PORT = "/dev/ttyAMA0"

def process_payload(payload):
    if len(payload) != PAYLOAD_SIZE:
        return False
    try:
        humidity, temperature, press, lux, status = struct.unpack('<ffffB', payload)
        print(f"{humidity:.2f} {temperature:.2f} {press:.2f} {lux:.2f} {status}")
        return True
    except struct.error:
        return False

def receive_packets():
    with serial.Serial(SERIAL_PORT,9600,timeout=0.8) as ser:
        print("opened serial")
        buffer = bytearray()
        last_send_time = time.time()
        while True:
            buffer.clear()
            ser.reset_input_buffer()
            ser.write(b'\xaa')
            ser.flush()
            start_time = time.time()
            packet_recieved = False

            while time.time() - start_time < 0.1:
                if ser.in_waiting > 0:
                    buffer.extend(ser.read(ser.in_waiting))
                start_idx = buffer.find(START_MARKER)
                if start_idx == -1:
                    if len(buffer) > len(START_MARKER):
                        buffer = buffer[-(len(START_MARKER)-1):]
                    continue
                if start_idx>0:
                    buffer = buffer[start_idx:]
                end_idx = buffer.find(END_MARKER,len(START_MARKER))
                if end_idx != -1:
                    payload = buffer[len(START_MARKER):end_idx]
                    process_payload(payload)
                    packet_recieved = True
                    buffer = buffer[end_idx+len(END_MARKER):]
            if not packet_recieved:
                print("NOT RECIEVED")
