import numpy as np
import matplotlib as plt
import yaml


class spectrum_graph:
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
        noise_floor_energetic is a high frequency wave (to look like static noise). 
        noise_floor_base is a very low frequency wave (to make the whole thing look wavy).
        '''

        # Create expression for energetic portion of noise floor
        noise_floor_energetic_amplitude = self.noise_floor_params['energetic_amplitude']
        noise_floor_energetic_frequency = self.noise_floor_params['energetic_frequency']

        noise_floor_energetic = noise_floor_energetic_amplitude * np.sin(noise_floor_energetic_frequency * self.frequency_range)

        # Create expression for base portion of noise floor
        noise_floor_base_amplitude = self.noise_floor_params['base_amplitude']
        noise_floor_base_frequency = self.noise_floor_params['base_frequency']

        noise_floor_base = noise_floor_base_amplitude * np.sin(noise_floor_base_frequency * self.frequency_range)

        # Add together each part including the base amplitude to make a squiggly wave that undulates up and down a bit
        noise_floor = self.noise_floor_params.base_amplitude + noise_floor_energetic + noise_floor_base

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

        plt.figure(figsize=(10,6))
        plt.plot(self.frequency_range, self.generate_spectrum_graph())
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.title('Spectrum Analyzer')
        plt.grid(True)
        plt.show()