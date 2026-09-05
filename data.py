# Save detector events in a daily CSV file that can be opened in a spreadsheet.
import csv
import os

from datetime import datetime
from pathlib import Path


# Keep the logger and display using the same folder, wherever they are launched.
DATA_FOLDER = Path(__file__).resolve().parent / "data"


def save_event(event):
    # Create the data folder if it does not already exist.
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Record the PC's local time when saving this event.
    now = datetime.now()

    # Use one file per day, named YYYY-MM-DD.csv.
    filename = os.path.join(
        DATA_FOLDER,
        now.strftime("%Y-%m-%d") + ".csv"
    )

    new_file = not os.path.exists(filename)

    # Append to the file; newline="" avoids extra blank lines on Windows.
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        # Add column headings only when creating a new file.
        if new_file:
            writer.writerow([
                "timestamp",
                "type",
                "event_number",
                "adc",
                "elapsed_ms",
                "dead_time_ms",
                "temperature",
                "pressure",
                "detector_id"
            ])

        # Write the timestamp and event values in the same order as the headings.
        writer.writerow([
            now.strftime("%Y-%m-%d %H:%M:%S"),
            event["type"],
            event["event_number"],
            event["adc"],
            event["elapsed_ms"],
            event["dead_time_ms"],
            event["temperature"],
            event["pressure"],
            event["detector_id"]
        ])
