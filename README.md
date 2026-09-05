# Simple PicoMuon logger and display

Run these commands from the repository root.

## Windows (PowerShell)

Install the dependencies:

```powershell
python -m pip install pyserial matplotlib
```

Set `PORT` in `main.py` to the detector's Windows COM port, for example:

```python
PORT = "COM7"
```

Find the correct COM number in Device Manager under **Ports (COM & LPT)**.
If using `pico_muon_test.py`, set its `PORT` to the same value.

Start the logger:

```powershell
python main.py
```

In a second terminal, open the daily display:

```powershell
python display.py
```

To view a previous day:

```powershell
python display.py --date 2026-09-05
```

## Raspberry Pi / Linux

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pyserial matplotlib
```

If virtual environment creation reports that `venv` is unavailable, run
`sudo apt install python3-venv` and retry.

Set `PORT` in `main.py` to the detector's Linux device path, normally:

```python
PORT = "/dev/ttyACM0"
```

Check available device paths with `ls /dev/ttyACM*`; the number may differ if
multiple devices are connected. If using `pico_muon_test.py`, change its `PORT`
to the same Linux device path. Both platforms use a baud rate of 115200.

Start the logger in the activated environment:

```bash
python main.py
```

In a second terminal, also opened at the repository root, activate the environment
and open the daily display:

```bash
source .venv/bin/activate
python display.py
```

To view a previous day:

```bash
python display.py --date 2026-09-05
```

The display needs a graphical desktop session. The logger can run from an SSH
terminal without a desktop. If opening the serial port gives a permission error
on Raspberry Pi OS, run `sudo usermod -aG dialout "$USER"`, then log out and back
in before retrying.

## Display and saved data

The display reads today's CSV every 10 seconds. It does not open the serial
port, so the logger can keep running. Close the plot window to stop the display;
press Ctrl+C in the logger terminal to stop logging.

Both scripts use the `data` folder beside these Python files, regardless of the
terminal's working directory. Restart an already-running logger to pick up this
folder change. Existing CSV files elsewhere are not moved automatically.

The graph counts saved C records in each local clock minute, using the PC
timestamps. The total is the number of C records in the file, not the detector's
cumulative counter. A minute with T or B records but no C records shows zero;
a minute without any records is left blank because logging coverage is unknown.
Partial minutes are not scaled to estimate a full-minute rate. This is a view of
recorded counts, without corrections for dead time or interruptions in logging.
