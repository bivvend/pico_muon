# Show the day's recorded muons while main.py continues to collect data.
import argparse
import csv
from datetime import date, datetime, time, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator

from data import DATA_FOLDER


REFRESH_SECONDS = 10


def read_day(day):
    # None means no recorded events in that minute, rather than zero muons.
    counts = [None] * 1440
    latest = None
    filename = DATA_FOLDER / f"{day:%Y-%m-%d}.csv"

    try:
        with open(filename, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                # Skip incomplete rows if the logger is still writing them.
                if None in row or any(value is None or value == "" for value in row.values()):
                    continue
                if row.get("type") not in ("T", "B", "C"):
                    continue
                try:
                    timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                except (KeyError, ValueError):
                    continue
                if timestamp.date() != day:
                    continue

                minute = timestamp.hour * 60 + timestamp.minute
                if counts[minute] is None:
                    counts[minute] = 0
                # Count C rows, not the detector's cumulative event number.
                if row["type"] == "C":
                    counts[minute] += 1
                latest = max(latest, timestamp) if latest else timestamp
    except FileNotFoundError:
        pass  # The display can start before the day's file exists.

    return counts, latest


def draw_day(ax, status, day):
    # Reload the CSV so newly logged events appear at the next refresh.
    counts, latest = read_day(day)
    start = datetime.combine(day, time.min)
    minutes = [start + timedelta(minutes=i) for i in range(1440)]
    values = [float("nan") if count is None else count for count in counts]
    total = sum(count for count in counts if count is not None)

    ax.clear()
    ax.plot(minutes, values, drawstyle="steps-post", marker=".", markersize=3)
    ax.set_title(f"UKRAA PicoMuon | {day:%d %B %Y}\nRecorded muons: {total:,}")
    ax.set_xlabel("Local time")
    ax.set_ylabel("Recorded muons per minute")
    ax.set_xlim(start, start + timedelta(days=1))
    ax.set_ylim(0, max(1, max((count or 0) for count in counts) * 1.15))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, alpha=0.25)

    if latest:
        status.set_text(f"Last recorded event: {latest:%H:%M:%S} | Refresh: {REFRESH_SECONDS}s")
    else:
        status.set_text(f"Waiting for recorded events in {day:%Y-%m-%d}.csv")


def main():
    parser = argparse.ArgumentParser(description="Display daily PicoMuon counts.")
    parser.add_argument("--date", type=date.fromisoformat, help="View a saved day: YYYY-MM-DD")
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.subplots_adjust(bottom=0.22, top=0.83)
    status = fig.text(0.5, 0.09, "", ha="center")
    fig.text(0.5, 0.035,
             "C events only. Blank minutes have no records. First/last minutes may be incomplete.",
             ha="center", fontsize=9)

    def refresh(_frame):
        # With no date argument, switch to the new day automatically at midnight.
        try:
            draw_day(ax, status, args.date or date.today())
        except OSError as error:
            status.set_text(f"Cannot read data; retrying in {REFRESH_SECONDS}s: {error}")

    # Keep the animation object alive for as long as the window is open.
    animation = FuncAnimation(fig, refresh, interval=REFRESH_SECONDS * 1000,
                              cache_frame_data=False)
    plt.show()


if __name__ == "__main__":
    main()
