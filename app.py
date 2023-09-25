from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import yaml

from web.forms import SettingsForm  # <--'SettingsForm' is the custom form to adjust signal parameters
from spectrum import spectrum

# Initialize the Flask App
app = Flask(__name__, template_folder='web/templates')
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection


# Initial root page. Renders the 'index.html' file showing an image of the Spectrum Analyzer
@app.route('/')
def index():
    
    # Create instance of spectrum graph and plot it
    spectrum_analyzer = spectrum('config/config.yaml')
    spectrum_analyzer.plot_spectrum_graph()

    return render_template('index.html')

# Settings modification page. Shows a form which is used to adjust the various signal parameters
@app.route('/settings', methods=['GET','POST'])
def settings():

    # Instantiate the form from the template
    form = SettingsForm()

    # Load the current configuration to populate the form
    with open('config/config.yaml', 'r') as f:
        current_config = yaml.load(f, Loader = yaml.FullLoader)


    if request.method == 'POST':
        if 'add_signal_spike' in request.form:
            # Handle adding a new signal spike
            form.signal_spike_params.append_entry()
        elif form.validate_on_submit:
            # Handle form submission to update the configuration
            config = {
                'frequency_range' : {
                    'start' : form.frequency_range_start.data,
                    'end' : form.frequency_range_end.data,
                    'num_points' : form.num_points.data
                },
                'noise_floor_params' : {
                    'base_amplitude': form.noise_floor_base_amplitude.data,
                    'high_energy_amplitude': form.noise_floor_high_energy_amplitude.data,
                    'high_energy_frequency': form.noise_floor_high_energy_frequency.data,
                    'low_energy_amplitude': form.noise_floor_low_energy_amplitude.data,
                    'low_energy_frequency': form.noise_floor_low_energy_frequency.data
                },
                'signal_spike_params' : [
                    {
                        'amplitude' : form.signal_spike_alpha_amplitude.data,
                        'mu' : form.signal_spike_alpha_mu.data,
                        'sigma': form.signal_spike_alpha_sigma.data,
                        'label' : "Signal Alpha"
                    },
                    {
                        'amplitude' : form.signal_spike_beta_amplitude.data,
                        'mu' : form.signal_spike_beta_mu.data,
                        'sigma': form.signal_spike_beta_sigma.data,
                        'label' : "Signal Beta"
                    },
                    {
                        'amplitude' : form.signal_spike_charlie_amplitude.data,
                        'mu' : form.signal_spike_charlie_mu.data,
                        'sigma': form.signal_spike_charlie_sigma.data,
                        'label' : "Signal Charlie"
                    },
                    {
                        'amplitude' : form.signal_spike_delta_amplitude.data,
                        'mu' : form.signal_spike_delta_mu.data,
                        'sigma': form.signal_spike_delta_sigma.data,
                        'label' : "Signal Delta"
                    },
                    {
                        'amplitude' : form.signal_spike_echo_amplitude.data,
                        'mu' : form.signal_spike_echo_mu.data,
                        'sigma': form.signal_spike_echo_sigma.data,
                        'label' : "Signal Echo"
                    },
                    {
                        'amplitude' : form.signal_spike_fox_amplitude.data,
                        'mu' : form.signal_spike_fox_mu.data,
                        'sigma': form.signal_spike_fox_sigma.data,
                        'label' : "Signal Fox"
                    }
                ]
            }

        # Save updated configuration to the config file
        with open('config/config.yaml', 'w') as f:
            yaml.dump(config, f)

        return redirect(url_for('index'))

    # Populate the Frequency Range fields with current config data
    form.frequency_range_start.default = current_config['frequency_range']['start']
    form.frequency_range_end.default = current_config['frequency_range']['end']
    form.num_points.default = current_config['frequency_range']['num_points']
    
    # Populate the Noise Floor fields with current config data
    form.noise_floor_base_amplitude.default = current_config['noise_floor_params']['base_amplitude']
    form.noise_floor_high_energy_amplitude.default = current_config['noise_floor_params']['high_energy_amplitude']
    form.noise_floor_high_energy_frequency.default = current_config['noise_floor_params']['high_energy_frequency']
    form.noise_floor_low_energy_amplitude.default = current_config['noise_floor_params']['low_energy_amplitude']
    form.noise_floor_low_energy_frequency.default = current_config['noise_floor_params']['low_energy_frequency']
    
    # Populate the Signal Spike fields with current config data
    form.signal_spike_alpha_amplitude.default = current_config['signal_spike_params'][0]['amplitude']
    form.signal_spike_alpha_mu.default = current_config['signal_spike_params'][0]['mu']
    form.signal_spike_alpha_sigma.default = current_config['signal_spike_params'][0]['sigma']
    
    form.signal_spike_beta_amplitude.default = current_config['signal_spike_params'][1]['amplitude']
    form.signal_spike_beta_mu.default = current_config['signal_spike_params'][1]['mu']
    form.signal_spike_beta_sigma.default = current_config['signal_spike_params'][1]['sigma']
    
    form.signal_spike_charlie_amplitude.default = current_config['signal_spike_params'][2]['amplitude']
    form.signal_spike_charlie_mu.default = current_config['signal_spike_params'][2]['mu']
    form.signal_spike_charlie_sigma.default = current_config['signal_spike_params'][2]['sigma']
    
    form.signal_spike_delta_amplitude.default = current_config['signal_spike_params'][3]['amplitude']
    form.signal_spike_delta_mu.default = current_config['signal_spike_params'][3]['mu']
    form.signal_spike_delta_sigma.default = current_config['signal_spike_params'][3]['sigma']
    
    form.signal_spike_echo_amplitude.default = current_config['signal_spike_params'][4]['amplitude']
    form.signal_spike_echo_mu.default = current_config['signal_spike_params'][4]['mu']
    form.signal_spike_echo_sigma.default = current_config['signal_spike_params'][4]['sigma']
    
    form.signal_spike_fox_amplitude.default = current_config['signal_spike_params'][5]['amplitude']
    form.signal_spike_fox_mu.default = current_config['signal_spike_params'][5]['mu']
    form.signal_spike_fox_sigma.default = current_config['signal_spike_params'][5]['sigma']


    # Process the form with current config data
    form.process(data=current_config)
    return render_template('settings.html', form=form)

# Static content page. Hosts images and other static content in case they need to be accessed directly.
@app.route('/static/<filename>')
def static_files(filename):
    # Serve static files (like the plot image) from the 'static' directory
    return send_from_directory('web/static', filename)

if __name__ == "__main__":
    app.run(debug=True)