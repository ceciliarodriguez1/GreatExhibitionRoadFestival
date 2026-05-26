# MoveSense Data Collector
## Description

MoveSense Data Collection is a Python-based command-line tool for collecting sensor data from MoveSense devices. It 
utilizes the Bleak library for Bluetooth communication and provides a customizable framework for connecting to multiple 
devices, subscribing to sensor data, and collecting and saving data in real-time.

Most of the MoveSense libraries offer data collection via mobile apps. This program aims to offer the same functionality
on desktop devices, with ease of connectivity to multiple devices and combining the collected data into single file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Firmware Installation](#firmware-installation)


## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/ceciliarodriguez1/GreatExhibitionRoadFestival.git
    ```

2. Navigate to the project directory:

    ```bash
    cd GreatExhibitionRoadFestival
    ```

3. Install the required dependencies:

    ```bash
    conda create -n GERFvenv python=3.10 -y
    conda activate GERFvenv
    pip install -r /rds/general/user/USERNAME/home/GERF/GreatExhibitionRoadFestival/requirements.txt
    ```

4. Connect to Movesense through CLI


5. Run the website

    ```bash
    streamlit run ../save_timestamp/website.py
    ```

## Usage

To start data collection using the CLI, follow these steps:

1. Ensure that MoveSense devices are turned on and discoverable.

2. (Optional) Create a session configuration file specifying the data output path, the devices and sensor paths.

    ```yaml
    output:
      path: outputs # Folder to which the data should be saved to
      filename:     # Filename template, which will be extended with
                    # a number when multiple data collections are done
   devices:         # List of adress-path objects.
   - address: 00:00:00:00:00:00 # MoveSense device address
      paths:                     # List of sensor paths to subscribe to
      - /Meas/Acc/13             # Find more details in MoveSense
                                 # official documentation.
    ```

3. Run the CLI, `--session` argument specifies the location of session config. If not provided
the CLI will look for "session.yaml" from root. If not found, a plain, empty session is initialized. Devices can be
connected to and paths subscribed to during runtime.

    ```bash
    python -m main  --session "session.yaml"
    ```

4. Follow the on-screen instructions to start and end data collection.

## Firmware Installation

For this CLI, the MoveSense devices require the `gatt-sensordata-app` firmware or the `default-firmware` version >=2.3.
I have used "Movesense-default_firmware-SS2_w_bootloader.zip" 

Official instructions for firmware update can be found here (and on the app):
- [MoveSense Firmware Installation Guide](https://www.movesense.com/docs/test_env/esw/dfu_update/)

The firmware installation requires a phone with the showcase app:
- [MoveSense ShowcaseApp Downloads](https://bitbucket.org/movesense/movesense-mobile-lib/downloads/)

And the firmware zip-file from:
- [MoveSense Firmware Downloads](https://bitbucket.org/movesense/movesense-device-lib/src/master/samples/bin/release/)

