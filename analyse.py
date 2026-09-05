# Analyse and plot all PicoMuon CSV files in the data folder.
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


DATA_FOLDER = Path(__file__).resolve().parent / "data"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_data():
    """Read every CSV file and return a list of event dictionaries."""
    events = []

    for filename in sorted(DATA_FOLDER.glob("*.csv")):
        with open(filename, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    event = {
                        "time": datetime.strptime(row["timestamp"], TIME_FORMAT),
                        "type": row["type"],
                        "adc": int(row["adc"]),
                        "elapsed_ms": int(row["elapsed_ms"]),
                        "dead_time_ms": int(row["dead_time_ms"]),
                        "temperature": float(row["temperature"]),
                        "pressure": float(row["pressure"]),
                    }
                except (KeyError, TypeError, ValueError):
                    # Ignore an incomplete row, for example while the logger is writing.
                    continue

                if event["type"] in ("T", "B", "C"):
                    events.append(event)

    return events


def print_summary(events):
    """Print a few useful numbers before showing the plots."""
    counts = Counter(event["type"] for event in events)

    print(f"Files analysed: {len(list(DATA_FOLDER.glob('*.csv')))}")
    print(f"Events analysed: {len(events):,}")
    print(f"Top events (T): {counts['T']:,}")
    print(f"Bottom events (B): {counts['B']:,}")
    print(f"Muon coincidences (C): {counts['C']:,}")

    if events:
        print(f"From: {min(event['time'] for event in events)}")
        print(f"To:   {max(event['time'] for event in events)}")
        print(f"Mean temperature: {average(events, 'temperature'):.2f} C")
        print(f"Mean pressure: {average(events, 'pressure'):.2f} hPa")


def average(events, field):
    """Return the average value of one field."""
    return sum(event[field] for event in events) / len(events)


def plot_data(events):
    """Make four simple plots from the recorded events."""
    times = [event["time"] for event in events]
    types = sorted(set(event["type"] for event in events))
    colours = {"T": "tab:blue", "B": "tab:orange", "C": "tab:green"}

    figure, axes = plt.subplots(2, 2, figsize=(12, 8))
    figure.suptitle("PicoMuon data analysis")

    # Plot 1: every event, so the different event types can be compared in time.
    for event_type in types:
        event_times = [event["time"] for event in events if event["type"] == event_type]
        axes[0, 0].plot(
            event_times,
            [event_type] * len(event_times),
            ".",
            label=event_type,
            color=colours[event_type],
            alpha=0.6,
        )
    axes[0, 0].set_title("Events over time")
    axes[0, 0].set_ylabel("Event type")
    axes[0, 0].legend(title="Type")

    # Plot 2: ADC values show the pulse-height distribution for each detector.
    for event_type in types:
        adc_values = [event["adc"] for event in events if event["type"] == event_type]
        axes[0, 1].hist(adc_values, bins=30, alpha=0.6, label=event_type,
                         color=colours[event_type])
    axes[0, 1].set_title("ADC value distribution")
    axes[0, 1].set_xlabel("ADC value")
    axes[0, 1].set_ylabel("Number of events")
    axes[0, 1].legend(title="Type")

    # Plot 3: environmental readings are repeated on each event row.
    axes[1, 0].plot(times, [event["temperature"] for event in events],
                    ".", markersize=3, label="Temperature")
    axes[1, 0].set_title("Temperature")
    axes[1, 0].set_ylabel("Temperature (C)")
    axes[1, 0].grid(True, alpha=0.25)

    # Plot 4: pressure has its own scale so small changes remain visible.
    axes[1, 1].plot(times, [event["pressure"] for event in events],
                    ".", markersize=3, color="tab:purple")
    axes[1, 1].set_title("Pressure")
    axes[1, 1].set_ylabel("Pressure (hPa)")
    axes[1, 1].grid(True, alpha=0.25)

    for axis in axes.flat:
        axis.set_xlabel("Time")
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        axis.tick_params(axis="x", rotation=30)

    figure.tight_layout()
    plt.show()


def main():
    events = read_data()

    if not events:
        print(f"No usable CSV data found in {DATA_FOLDER}")
        return

    print_summary(events)
    plot_data(events)


if __name__ == "__main__":
    main()