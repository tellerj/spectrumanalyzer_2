from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from datetime import datetime
import yaml
import argparse


# Custom modules/imports for this project
from web.forms import SettingsForm  # <--'SettingsForm' is the custom form to adjust signal parameters
from spectrum import Spectrum

# Initialize the Flask App
app = Flask(__name__, template_folder='web/templates')
app.secret_key = '32wps'  # Flask requirement to enable CSRF protection as well as the 'flash' method functionality
app.config['SECRET_KEY'] = '32wps'

# Parse command-line arguments, mainly to handle a user-specified config path
def parse_args():
    parser = argparse.ArgumentParser(description='Spectrum Analyzer Web App')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                        help='Path to the initial config file (default: config/config.yaml)')
    args = parser.parse_args()
    return args

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

# Helper function to update the running config
def update_running_config(form):
    # Update the running config with form submission values
    global running_config

    # Frequency Range Settings
    running_config['frequency_range_start'] = form.frequency_range_start.data
    running_config['frequency_range_end'] = form.frequency_range_end.data
    running_config['frequency_range_num_points'] = form.frequency_range_num_points.data
    
    # Noise Floor Settings
    running_config['noise_floor_params_base_amplitude'] = form.noise_floor_base_amplitude.data
    running_config['noise_floor_params_high_energy_amplitude'] = form.noise_floor_high_energy_amplitude.data
    running_config['noise_floor_params_high_energy_frequency'] = form.noise_floor_high_energy_frequency.data
    running_config['noise_floor_params_low_energy_amplitude'] = form.noise_floor_low_energy_amplitude.data
    running_config['noise_floor_params_low_energy_frequency'] = form.noise_floor_low_energy_frequency.data
    
    # Signal Spike Settings
    for i in range(5):
        running_config[f'signal_spike_{i}_amplitude'] = form[f'signal_spike_{i}_amplitude'].data
        running_config[f'signal_spike_{i}_mu'] = form[f'signal_spike_{i}_mu'].data
        running_config[f'signal_spike_{i}_sigma'] = form[f'signal_spike_{i}_sigma'].data

# Initialize a global variable to store the running config
args = parse_args()
running_config = load_config(args.config)

# Initial root page. Renders the 'index.html' file showing an image of the Spectrum Analyzer
@app.route('/')
def index():
    # Create instance of spectrum graph and plot it
    spectrum_analyzer = Spectrum(running_config)
    animation_html = spectrum_analyzer.animate_spectrum()
    return render_template('index.html', animation_html=animation_html)

# Settings modification page. Shows a form which is used to adjust the various signal parameters
@app.route('/settings', methods=['GET','POST'])
def settings():

    global running_config

    # Instantiate the form from the template
    form = SettingsForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Update the running config with form submission values
        update_running_config(form)
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    

    # # Populate the Frequency Range fields with current config data
    # form.frequency_range_start.default = running_config['frequency_range']['start']
    # form.frequency_range_end.default = running_config['frequency_range']['end']
    # form.num_points.default = running_config['frequency_range']['num_points']
    
    # # Populate the Noise Floor fields with current config data
    # form.noise_floor_base_amplitude.default = running_config['noise_floor_params']['base_amplitude']
    # form.noise_floor_high_energy_amplitude.default = running_config['noise_floor_params']['high_energy_amplitude']
    # form.noise_floor_high_energy_frequency.default = running_config['noise_floor_params']['high_energy_frequency']
    # form.noise_floor_low_energy_amplitude.default = running_config['noise_floor_params']['low_energy_amplitude']
    # form.noise_floor_low_energy_frequency.default = running_config['noise_floor_params']['low_energy_frequency']
    
    # # Populate the Signal Spike fields with current config data
    # form.signal_spike_0_amplitude.default = running_config['signal_spike_params'][0]['amplitude']
    # form.signal_spike_0_mu.default = running_config['signal_spike_params'][0]['mu']
    # form.signal_spike_0_sigma.default = running_config['signal_spike_params'][0]['sigma']
    
    # form.signal_spike_1_amplitude.default = running_config['signal_spike_params'][1]['amplitude']
    # form.signal_spike_1_mu.default = running_config['signal_spike_params'][1]['mu']
    # form.signal_spike_1_sigma.default = running_config['signal_spike_params'][1]['sigma']
    
    # form.signal_spike_2_amplitude.default = running_config['signal_spike_params'][2]['amplitude']
    # form.signal_spike_2_mu.default = running_config['signal_spike_params'][2]['mu']
    # form.signal_spike_2_sigma.default = running_config['signal_spike_params'][2]['sigma']
    
    # form.signal_spike_3_amplitude.default = running_config['signal_spike_params'][3]['amplitude']
    # form.signal_spike_3_mu.default = running_config['signal_spike_params'][3]['mu']
    # form.signal_spike_3_sigma.default = running_config['signal_spike_params'][3]['sigma']
    
    # form.signal_spike_4_amplitude.default = running_config['signal_spike_params'][4]['amplitude']
    # form.signal_spike_4_mu.default = running_config['signal_spike_params'][4]['mu']
    # form.signal_spike_4_sigma.default = running_config['signal_spike_params'][4]['sigma']
    
    # form.signal_spike_5_amplitude.default = running_config['signal_spike_params'][5]['amplitude']
    # form.signal_spike_5_mu.default = running_config['signal_spike_params'][5]['mu']
    # form.signal_spike_5_sigma.default = running_config['signal_spike_params'][5]['sigma']

    # Process the form with current config data
    form.process(obj=running_config)
    return render_template('settings.html', form=form)

# Static content page. Hosts images and other static content in case they need to be accessed directly.
@app.route('/static/<filename>')
def static_files(filename):
    # Serve static files (like the plot image) from the 'static' directory
    return send_from_directory('web/static', filename)

# Page to handle saving off the current config -- triggered via POST
@app.route('/save_config', methods=['POST'])
def save_config():
    # Access the global running config
    global running_config

    # Generate a date-timestamp string
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M-%S")

    # Construct a new filename with the timestamp
    filename = f'config/config_{timestamp}.yaml'

    #Save the running config to a file
    with open (filename, 'w') as f:
        yaml.dump(running_config, f)

    flash(f'Config saved successfully as {filename}', 'success')
    return redirect(url_for('settings'))

if __name__ == "__main__":
    app.run(debug=True)