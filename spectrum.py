import numpy as np
import matplotlib.pyplot as plt
import yaml
import os


class spectrum:
    """
    A class representing a spectrum graph.

    Attributes
    --------------
    ...


    Methods
    --------------
    ...
    """

    def __init__(self, config):
        self.config = config
        self.initialize_parameters()

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    def initialize_parameters(self):
        #Extract Frequency Range parameters from config
        self.frequency_range = np.linspace(
            self.config['frequency_range_start'],
            self.config['frequency_range_end'],
            self.config['frequency_range_num_points']
        )

        # Extract Noise Floor parameters from config
        self.noise_floor_base_amplitude = self.config['noise_floor_base_amplitude']
        self.noise_floor_high_energy_amplitude = self.config['noise_floor_high_energy_amplitude']
        self.noise_floor_high_energy_frequency = self.config['noise_floor_high_energy_frequency']
        self.noise_floor_low_energy_amplitude = self.config['noise_floor_low_energy_amplitude']
        self.noise_floor_low_energy_frequency = self.config['noise_floor_low_energy_frequency']

        # Extract Signal Spike parameters from config
        self.signal_spike_0_amplitude = self.config['signal_spike_0_amplitude']
        self.signal_spike_0_mu = self.config['signal_spike_0_mu']
        self.signal_spike_0_sigma = self.config['signal_spike_0_sigma']
        
        self.signal_spike_1_amplitude = self.config['signal_spike_1_amplitude']
        self.signal_spike_1_mu = self.config['signal_spike_1_mu']
        self.signal_spike_1_sigma = self.config['signal_spike_1_sigma']
        
        self.signal_spike_2_amplitude = self.config['signal_spike_2_amplitude']
        self.signal_spike_2_mu = self.config['signal_spike_2_mu']
        self.signal_spike_2_sigma = self.config['signal_spike_2_sigma']
        
        self.signal_spike_3_amplitude = self.config['signal_spike_3_amplitude']
        self.signal_spike_3_mu = self.config['signal_spike_3_mu']
        self.signal_spike_3_sigma = self.config['signal_spike_3_sigma']
        
        self.signal_spike_4_amplitude = self.config['signal_spike_4_amplitude']
        self.signal_spike_4_mu = self.config['signal_spike_4_mu']
        self.signal_spike_4_sigma = self.config['signal_spike_4_sigma']
        
        self.signal_spike_5_amplitude = self.config['signal_spike_5_amplitude']
        self.signal_spike_5_mu = self.config['signal_spike_5_mu']
        self.signal_spike_5_sigma = self.config['signal_spike_5_sigma']

    def generate_spectrum_graph(self):
        '''
        Generate a graph of the spectrum, using noise floor and variable number of signal spikes
        '''

        noise_floor = self.generate_noise_floor()
        signal_spikes = self.generate_signal_spikes()

        # sum the noise floor and signal spikes to get the final expression of the curve
        spectrum_graph = noise_floor + signal_spikes

        return spectrum_graph
    
    
    def generate_noise_floor(self):
        '''
        Generate noise floor data (e.g. high-frequency sine wave). It's actually two waves. 
        noise_floor_high_energy is a high frequency wave (to look like static noise). 
        noise_floor_low_energy is a very low frequency wave (to make the whole thing look wavy).
        '''

        # Create expression for energetic portion of noise floor
        noise_floor_high_energy = self.noise_floor_high_energy_amplitude * np.sin(self.noise_floor_high_energy_frequency * self.frequency_range)

        # Create expression for base portion of noise floor
        noise_floor_low_energy = self.noise_floor_low_energy_amplitude * np.sin(self.noise_floor_low_energy_frequency * self.frequency_range)

        # Add together each part including the base amplitude to make a squiggly wave that undulates up and down a bit
        noise_floor = self.noise_floor_base_amplitude + noise_floor_low_energy + noise_floor_high_energy 

        return noise_floor
    
    
    def generate_signal_spikes(self):
        '''
        Generate signal spikes (e.g. Gaussian curves) as many times as there are configured parameters
        '''
        # Make an array of zeroes the same length as the frequency range of the graph
        signal_spikes = np.zeros_like(self.frequency_range)

        # Iterate through each set of spike parameters and compute Gaussian Curve for that spike, add to signal_spikes array
        for i in range(5):
            amp =  self.config[f'signal_spike_{i}_amplitude']   # Height of the spike
            mu = self.config[f'signal_spike_{i}_mu']            # Center-frequency of the spike
            sigma = self.config[f'signal_spike_{i}_sigma']      # Width of the spike

            signal_spikes += amp * np.exp( -0.5 * ( (self.frequency_range - mu) ** 2) / (sigma ** 2) )

        return signal_spikes
    
    
    def plot_spectrum_graph(self):
        '''
        Create a matplotlib plot of the spectrum graph
        '''

        plt.figure(figsize=(18,8))
        plt.plot(self.frequency_range, self.generate_spectrum_graph())
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.title('Spectrum Analyzer')
        plt.grid(True)

        # Set image path
        image_path = 'web/static/spectrum_plot.png'

        # If there's an old image there, delete it first
        if os.path.exists(image_path):
            os.remove(image_path)

        # Save the plot as an image in the static folder
        plt.savefig(image_path)

        # Close the plot to save resources
        plt.close()