## Prerequisites

- CSV sheet of sound data as collected from the Analog Discovery 2 device.

## Usage

here you can see multiple python scripts, each one of them is responsible for a different task.

# Calibration

This script is responsible for calculating the current speed of sound.
note: the data should be of a sound emitter located at (0,0)

# Localization

This script is responsible for calculating the location of the sound emitter by doing all the required calculations from the data sheet.

to use this script with an embedded device, the source of the data should be changed to a UART port instead of the CSV file.
