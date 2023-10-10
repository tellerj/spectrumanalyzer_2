# Spectrum Analyzer Web Application

The Spectrum Analyzer Web Application is a tool for visualizing and configuring spectrum data. It allows you to generate animated spectrum plots with signal spikes and noise floor settings.

## Table of Contents

- [Spectrum Analyzer Web Application](#spectrum-analyzer-web-application)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation Steps](#installation-steps)
  - [Usage](#usage)
  - [Improvements Needed](#improvements-needed)

## Features

- Visualize spectrum data with animated plots.
- Configure frequency range, noise floor settings, and signal spikes.
- Dynamically add or remove signal spike configurations.
- Save and load configuration settings.
- Responsive web interface for easy access.

## Requirements

- Python 3.x
- Flask
- Matplotlib
- NumPy
- and others

## Installation Steps

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/tellerj/spectrumanalyzer_2.git
   cd spectrumanalyzer_2
   ```

2. Install Dependencies (included)

    ```bash
    pip install --no-index -r /dependencies/requirements.txt --find-links=/dependencies/packages
    ```

3. (Optional, recommended) Create Virtual Environment

    ```bash
    python -m pipenv install
    pipenv install
    pipenv shell
    ```

4. Start the Application

    ```bash
    python app.py
    ```
    The application should now be running at `http://localhost:5000`
    
    *NOTE: Initial startup takes about a minute and 32 seconds since the animation must be generated.wait for `[+] Spectrum animation generated.` console message.*

## Usage

- Access the application at `http://localhost:5000`

- Adjust the parameters of the displayed animation by clicking on the `Settings` link or navigating to `http://localhost:5000/settings`

- The application ingests a `config.yaml` file on startup, and can you export the current config by clicking the `Save Config` button at the bottom of the Settings page. An example config is included, and looks has three main sections: 

**Frequency Range Parameters**
```yaml
frequency_range_start: 100
frequency_range_end: 300  # Define your frequency range in Hz
frequency_range_num_points: 2000  # Number of data points to plot. More will make the line smoother, but will slow down the animation generation. 10 points per Hz seems to be a good balance (i.e. if freq range is 100, number of points should be ~1000)
```

**Noise Floor Parameters**

Noise floor is made of a sine wave with randomness multiplied in to make it look shakey.

```yaml
noise_floor_base_amplitude: 10.0 # Overall base amplitude of the noise floor (where it will center around on the y-axis)
noise_floor_high_energy_amplitude: 3.0  # Amplitude of the high_energy part of the noise floor
noise_floor_high_energy_frequency: 3  # Frequency of the high_energy part of the noise floor in Hz
```

**Signal Spike Parameters**

Signal spikes are modeled as [Gaussian functions](https://en.wikipedia.org/wiki/Gaussian_function) where:
- Amplitude = Height of signal spike
- Mu = Center point of signal spike
- Sigma = Width of signal spike

```yaml
signal_spike_0_amplitude: 50.0
signal_spike_0_mu: 114.0
signal_spike_0_sigma: 2.0

signal_spike_1_amplitude: 55.0
signal_spike_1_mu: 140.0
signal_spike_1_sigma: 2.0

...
```

## Improvements Needed
- Add/Remove signal spike forms on the settings page using buttons
- Add buttons for scenarios such as:
    - Remote signal offline
    - Rain over remote site
    - Rain over local site