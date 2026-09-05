# Handle the serial connection and convert incoming text into event data.
import serial


def connect(port, baud_rate=115200):
    # Wait up to two seconds for a read before returning any available data.
    return serial.Serial(
        port=port,
        baudrate=baud_rate,
        timeout=2
    )


def read_line(serial_port):
    # Read bytes up to a newline, or until the timeout expires.
    raw = serial_port.readline()

    # Return None when no bytes arrived.
    if not raw:
        return None

    # Convert bytes to text and remove surrounding whitespace and line endings.
    return raw.decode("utf-8", errors="ignore").strip()


def parse_line(line):
    # Each event is expected to contain eight comma-separated fields.
    parts = line.split(",")

    if len(parts) != 8:
        return None

    # T = top detector, B = bottom detector, C = coincidence (muon).
    if parts[0] not in ["T", "B", "C"]:
        return None

    # Give each field a name and convert numeric text to numbers.
    try:
        return {
            "type": parts[0],
            "event_number": int(parts[1]),
            "adc": int(parts[2]),
            "elapsed_ms": int(parts[3]),
            "dead_time_ms": int(parts[4]),
            "temperature": float(parts[5]),
            "pressure": float(parts[6]),
            "detector_id": parts[7]
        }

    # Ignore the line if a numeric field cannot be converted.
    except ValueError:
        return None
