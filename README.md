# Simple PicoMuon logger and display

Install the dependencies:

```powershell
python -m pip install pyserial matplotlib
```

From the repository root, start the logger:

```powershell
python emanuel/main.py
```

In a second terminal, open the daily display:

```powershell
python emanuel/display.py
```

The display reads today's CSV every 10 seconds. It does not open the serial
port, so the logger can keep running. Close the plot window to stop the display;
press Ctrl+C in the logger terminal to stop logging.

To view a previous day:

```powershell
python emanuel/display.py --date 2026-09-05
```

Both scripts use the `data` folder beside these Python files, regardless of the
terminal's working directory. Restart an already-running logger to pick up this
folder change. Existing CSV files elsewhere are not moved automatically.

The graph counts saved C records in each local clock minute, using the PC
timestamps. The total is the number of C records in the file, not the detector's
cumulative counter. A minute with T or B records but no C records shows zero;
a minute without any records is left blank because logging coverage is unknown.
Partial minutes are not scaled to estimate a full-minute rate. This is a view of
recorded counts, without corrections for dead time or interruptions in logging.
