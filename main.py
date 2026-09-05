# Read detector events, save them to CSV, and display muon detections.
from detector import connect, read_line, parse_line
from data import save_event


# Serial port and communication speed for the attached detector.
PORT = "COM7"
BAUD_RATE = 115200


def main():

    print("PicoMuon data logger")
    print("--------------------")

    # Open the connection, or show an error if the detector is unavailable.
    try:
        serial_port = connect(PORT, BAUD_RATE)

    except Exception as error:
        print(f"Could not connect to {PORT}")
        print(error)
        return

    print(f"Connected to {PORT}")
    print("Waiting for detector events...")
    print("Press Ctrl+C to stop.\n")

    try:

        # Keep reading events until the user presses Ctrl+C.
        while True:

            line = read_line(serial_port)

            # A timeout with no data is normal; keep waiting.
            if line is None:
                continue

            # Turn the comma-separated text into named event values.
            event = parse_line(line)

            # Show unrecognised lines, but do not store them as events.
            if event is None:
                print("Unknown data:", line)
                continue

            # Store all top (T), bottom (B), and coincidence (C) events.
            save_event(event)

            # Only coincidences count as muon detections for this display.
            # The count comes from the detector, not from this script's start time.
            if event["type"] == "C":
                print(
                    f"MUON  "
                    f"Count: {event['event_number']}  "
                    f"ADC: {event['adc']}  "
                    f"Temp: {event['temperature']} C  "
                    f"Pressure: {event['pressure']} hPa"
                )

    except KeyboardInterrupt:
        print("\nStopping PicoMuon logger.")

    # Close the connection when stopping, including after an error.
    finally:
        serial_port.close()


# Start the logger when this file is run directly.
if __name__ == "__main__":
    main()
