# Quick connection check: display incoming text without parsing or saving it.
import serial
from datetime import datetime

# Serial port and communication speed for the attached detector.
PORT = "COM7"
BAUD_RATE = 115200

print(f"Connecting to PicoMuon on {PORT}...")

try:
    # Open the connection with 8 data bits, no parity, and 1 stop bit.
    # The with block closes the connection automatically when it ends.
    with serial.Serial(
        port=PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2
    ) as ser:

        print("Connected.")
        print("Waiting for data...\n")

        # Keep reading until Ctrl+C is pressed or a serial error occurs.
        while True:
            line = ser.readline()

            # Ignore empty reads caused by the timeout.
            if line:
                # Convert bytes to text and add the PC's local time for display.
                text = line.decode("utf-8", errors="ignore").strip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print(f"{timestamp}  |  {text}")

# Report connection problems, such as an unavailable or disconnected port.
except serial.SerialException as e:
    print(f"\nSerial error: {e}")

# Stop cleanly when the user presses Ctrl+C.
except KeyboardInterrupt:
    print("\nStopped.")
