import serial
import csv
import time

# --- CONFIGURATION ---
SERIAL_PORT = 'COM8'
BAUD_RATE = 115200
OUTPUT_FILE = 'serial_log.csv'

try:
    # Open serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for Arduino reset

    print("Connected to", SERIAL_PORT)

    # Open CSV file
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Timestamp","Value"])

        while True:
            try:
                # Read line from serial
                line = ser.readline().decode('utf-8').strip()

                if line:
                    timestamp = time.time()  # UNIX timestamp
                    
                    print(f"{timestamp}, {line}")

                    # Write to CSV
                    writer.writerow([timestamp,line])
                    file.flush()  # ensure real-time writing

            except Exception as e:
                print("Read error:", e)

except Exception as e:
    print("ERROR:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed")