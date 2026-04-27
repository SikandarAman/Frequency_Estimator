import serial
import numpy as np
from collections import deque
import time

# --- CONFIGURATION ---
SERIAL_PORT = 'COM14' 
BAUD_RATE = 115200
N = 5
FS = 10000
TS = 1/FS

data_buffer = deque(maxlen=2*N)
zc_region_tz = []
last_Tc = None

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"--- Connected to {SERIAL_PORT} ---")
except Exception as e:
    print(f"--- ERROR: Could not open port: {e} ---")
    exit()

print("System Online. Processing live data...")

prev = 0
try:
    while True:
        # GATE 1: Is there any data at all?
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # GATE 2: Is the data readable?
                if not line:
                    continue
                
                scaled_val = int(line)
                data_buffer.append(scaled_val)
                
                # GATE 3: Is the buffer full yet?
                # (Prints once every 100 samples to avoid flooding the screen)
                if len(data_buffer) < 2*N:
                    if len(data_buffer) % 10 == 0:
                        print(f"Filling buffer... {len(data_buffer)}/{2*N}")
                    continue
                
                # WINDOW LOGIC
                current_data = list(data_buffer)
                m1 = np.mean(current_data[0:N])
                m2 = np.mean(current_data[N:2*N])
                
                # GATE 4: Diagnostic - What are the averages?
                # This will print the raw values so you can see if it's even near zero
                # if time.time() % 1 < 0.01: # Limit print to roughly once per second
                #     print(f"Debug Stats -> Val: {scaled_val} | M1: {m1:.1f} | M2: {m2:.1f}")

                current_time = time.perf_counter()
                
                # GATE 5: SIGN CHANGE DETECTION
                if m1 * m2 < 0:
                    den = 2 * (m1 - m2)
                    if abs(den) > 1e-12:
                        tz = current_time - N*TS*(1 - (m1 + m2)/den)
                        zc_region_tz.append(tz)
                        # Uncomment next line to see every "hit"
                        # print("Hit region...")
                else:
                    # Region ended
                    if len(zc_region_tz) > 0:
                        Tc = np.mean(zc_region_tz)
                        # print(f"--- Zero Crossing Detected at {Tc:.4f} ---")
                        
                        if last_Tc is not None:
                            period = 2 * (Tc - last_Tc)
                            if period > 0:
                                
                                cur = (1 / period)
                                freq = (cur+prev)/2
                                print(f"===> CALCULATED FREQUENCY: {freq:.2f} Hz <===")
                                prev = cur

                        last_Tc = Tc
                        zc_region_tz = []

            except ValueError:
                print(f"Corrupted data received: {line}")
                continue

except KeyboardInterrupt:
    print("Closing...")
    ser.close()