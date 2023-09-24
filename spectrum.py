import numpy as np
import matplotlib.pyplot as plt
import yaml


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

    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.initialize_parameters()

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    def initialize_parameters(self):
        #Extract Frequency Range parameters from config
        self.frequency_range = np.linspace(
            self.config['frequency_range']['start'],
            self.config['frequency_range']['end'],
            self.config['frequency_range']['num_points']
        )

        # Extract Noise Floor parameters from config
        self.noise_floor_params = self.config['noise_floor_params']

        # Extract Signal Spike parameters from config
        self.signal_spike_params = self.config['signal_spike_params']



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
        noise_floor_high_energy_amplitude = self.noise_floor_params['high_energy_amplitude']
        noise_floor_high_energy_frequency = self.noise_floor_params['high_energy_frequency']

        noise_floor_high_energy = noise_floor_high_energy_amplitude * np.sin(noise_floor_high_energy_frequency * self.frequency_range)

        # Create expression for base portion of noise floor
        noise_floor_low_energy_amplitude = self.noise_floor_params['low_energy_amplitude']
        noise_floor_low_energy_frequency = self.noise_floor_params['low_energy_frequency']

        noise_floor_low_energy = noise_floor_low_energy_amplitude * np.sin(noise_floor_low_energy_frequency * self.frequency_range)

        # Add together each part including the base amplitude to make a squiggly wave that undulates up and down a bit
        noise_floor = self.noise_floor_params['base_amplitude'] + noise_floor_low_energy + noise_floor_high_energy 

        return noise_floor
    
    
    def generate_signal_spikes(self):
        '''
        Generate signal spikes (e.g. Gaussian curves) as many times as there are configured parameters
        '''
        # Make an array of zeroes the same length as the frequency range of the graph
        signal_spikes = np.zeros_like(self.frequency_range)

        # Iterate through each set of spike parameters and compute Gaussian Curve for that spike, add to signal_spikes array
        for spike in self.signal_spike_params:
            amp = spike['amplitude']    # Height of the spike
            mu = spike['mu']            # Center-frequency of the spike
            sigma = spike['sigma']      # Width of the spike

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

        # Save the plot as an image in the static folder
        plt.savefig('web/static/spectrum_plot.png')

        # Close the plot to save resources
        plt.close()