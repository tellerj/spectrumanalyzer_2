import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

config = {
    'freq_range_start' : 0,
    'freq_range_end' : 1000,
    'freq_range_steps' : 1001,
    'noise_floor_base' : 20,
    'noise_floor_amp' : 3,
    'noise_floor_freq' : 100,
    'signal_spike_0_amp': 40,
    'signal_spike_0_mu' : 300,
    'signal_spike_0_sigma' : 10
}

class Spectrum:
    def __init__(self, ax, config):
        self.ax = ax
        self.config = config
        self.freq_range = range(self.config['freq_range_start'], self.config['freq_range_end'])
        self.pointer = 0
        self.new_x_vals = [0]
        self.new_y_vals = [0]
        self.x_vals = [0]   #np.zeros(len(self.freq_range))  #np.full(len(self.freq_range), None)
        self.y_vals = [0]   #np.zeros(len(self.x_vals))   #np.full(len(self.x_vals), None)
        self.line = Line2D(self.x_vals, self.y_vals)
        self.ax.add_line(self.line)
        self.ax.set_xlim(self.config['freq_range_start'], self.config['freq_range_end'])
        self.ax.set_ylim(0, 100)

    def generate_line(self):
        for i in range(len(self.freq_range)):
            self.x_vals.append(i)
            self.y_vals.append(next(self.signal_emitter()))
        self.line.set_data(self.x_vals, self.y_vals)
        return self.line,

    def update(self, y):
        lastx = self.new_x_vals[-1]
        if lastx >= self.freq_range[-5]:
            self.new_x_vals = [0]
            self.new_y_vals = [0]
            self.ax.set_xlim(self.x_vals[0], self.config['freq_range_end'])
            self.ax.figure.canvas.draw()

        x = self.freq_range[len(self.new_x_vals) + 1]

        self.new_x_vals.append(x)
        self.new_y_vals.append(y)
        for i in range(len(self.new_x_vals)):
            self.x_vals[i] = self.new_x_vals[i]
            self.y_vals[i] = self.new_y_vals[i]
            self.y_vals[i+1] = None
            self.y_vals[i+2] = None
            self.y_vals[i+3] = None
            self.y_vals[i+4] = None
            self.y_vals[i+5] = None

        self.line.set_data(self.x_vals, self.y_vals)
        return self.line,

    def signal_emitter(self):
        rint = np.random.randint(-2,2)
        rval = np.random.rand()
        noise_floor = rint + self.config['noise_floor_base'] + rval * self.config['noise_floor_amp'] * np.sin(np.random.rand() * self.config['noise_floor_freq'] * self.x_vals[-1])
        signal_spike = self.config['signal_spike_0_amp'] * np.exp( -0.5 * ( (self.new_x_vals[-1] - self.config['signal_spike_0_mu']) ** 2) / (self.config['signal_spike_0_sigma'] ** 2) )
        yield noise_floor + signal_spike
            

fig, ax = plt.subplots()
spectrum = Spectrum(ax, config)
spectrum.generate_line()


ani = FuncAnimation(fig, spectrum.update, spectrum.signal_emitter, interval=10, blit=True, save_count=100, repeat=True)

plt.show()