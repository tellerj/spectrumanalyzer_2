import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np 
import yaml
from IPython.display import HTML as html

plt.rcParams['animation.ffmpeg_path'] = "C:\\Users\\telle\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-6.0-full_build\\bin\\ffmpeg.exe"

class Spectrum:
    def __init__(self,config = None):
        self.config = config
        self.frequency_range_start = self.config['frequency_range_start'] - 35
        self.frequency_range_end = self.config['frequency_range_end'] + 35
        self.frequency_range = range(self.frequency_range_start, self.frequency_range_end)
        self.num_spikes = self.count_spikes()
        self.pointer = 0
        self.frames = 3 * (len(self.frequency_range))
        self.dt = .1

        #Set up the plot, styling, size, etc.
        fig_width = .80 * 1920  # 80% of 1080p display width
        fig_height = .7 * 1080 # 70% of 1080p display height
        self.fig, self.axis = plt.subplots(facecolor='grey', figsize=(fig_width / 80, fig_height / 80)) # Divide by 80 for dpi adjustment
        self.axis.grid(True, color='darkgrey', lw=.5)
        self.axis.set_facecolor('black')
        self.axis.set_title('Spectrum Analzer')
        self.axis.set_xlabel("Frequency (MHz)")
        self.axis.set_ylabel("Amplitude (%)")
        self.axis.set_xlim(self.config['frequency_range_start'], self.config['frequency_range_end'])
        self.axis.set_ylim(0, 100)
        self.xdata, self.ydata = [],[]
        for i in self.frequency_range:
            self.xdata.append(None)
            self.ydata.append(None)
        self.line, = self.axis.plot([],[], lw = 1, color='lightgreen')

    def count_spikes(self):
        '''Count the number of signal spikes in the current config'''
        count = 0
        for key in self.config.keys():
            if key.startswith('signal_spike_') and key.endswith('_amplitude'): # Obviously...doesn't check that all necessary parameters are present
                count += 1
        return count
    
    def save_animation(self, filename):
        anim = self.gen_animation()
        anim.save(filename, writer='ffmpeg', fps=30)

    def init(self): 
        for i in self.frequency_range:
            self.animate(i)
        return self.line, 

    # animation function 
    def animate(self, i): 

        pt = self.pointer

        # break early if we're close to the end of the line
        # this is to avoid 'index out of range' when clearing the next 5 points, below
        if pt >= len(self.frequency_range) - 3:
            self.pointer = 0
            pt = 0
    
        # t is a parameter which varies 
        # with the frame number 'i', by amount 'self.dt'
        x = self.frequency_range[pt]

        # Compute messy looking noise floor, using some random multipliers
        rint = np.random.randint(-2,2)
        rfloat = np.random.rand()
        n_base = self.config['noise_floor_base_amplitude']
        n_amp = self.config['noise_floor_high_energy_amplitude']
        n_freq = self.config['noise_floor_high_energy_frequency']
        
        #noise_floor = n_base + n_amp * np.sin(n_freq * x)
        noise_floor_value = rint + n_base + rfloat * n_amp * np.sin(n_freq * x)

        # Iterate through each set of spike parameters and compute Gaussian Curve for that spike, add to signal_spikes array
        signal_spike_value = 0
        for j in range(self.num_spikes):
            s_amp =  self.config[f'signal_spike_{j}_amplitude']   # Height of the spike
            s_mu = self.config[f'signal_spike_{j}_mu']            # Center-frequency of the spike
            s_sigma = self.config[f'signal_spike_{j}_sigma']      # Width of the spike

            try:
                signal_spike_value += s_amp * np.exp( -0.5 * ( (x - s_mu) ** 2) / (s_sigma ** 2) )

                # Add a label at the center frequency of the signal spike
                if x == s_mu:
                    self.axis.annotate(f"+\n|\n|\nSignal {j}\n{x} MHz", (s_mu, 0), xytext=(0, 0), textcoords='offset points', ha='center', va='bottom', rotation=0, color='white')

            except: 
                continue
        
        # Technically, this is wrong. 
        # Adding the values together would be computing the 'superposition' of the signals
        # What we should actually do is compute the convolution of the signals (np.convolve())
        y = noise_floor_value + signal_spike_value

        # change existing x and y values to newly computed ones
        self.xdata[pt] = x
        self.ydata[pt] = y

        # clear the next few points to make it look like a cursor
        self.ydata[pt+1] = None
        self.ydata[pt+2] = None
        self.ydata[pt+3] = None

        #set line data to newly updated set of points
        self.line.set_data(self.xdata, self.ydata)

        self.pointer +=1
        
        return self.line, 

    def gen_animation(self, format=None):

        # calling the animation function	 
        anim = animation.FuncAnimation(
            self.fig, 
            self.animate,  
            frames = self.frames,
            init_func=self.init,
            interval = 15, 
            blit = True, 
            repeat = True)

        if format == 'jshtml':
            return anim.to_jshtml()
        elif format == 'html5_video':
            return anim.to_html5_video()
        
        return anim
    
    

# with open('config/config.yaml', 'r') as f:
#     config = yaml.load(f, Loader=yaml.FullLoader)
# spectrum = Spectrum(config)
# anim = spectrum.gen_animation() #.save('growingCoil1.mp4', writer = 'ffmpeg', fps = 30)
# plt.show()

# saves the animation in our desktop 
#anim.save('growingCoil.mp4', writer = 'ffmpeg', fps = 30) 
