from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify
from datetime import datetime
import yaml
import argparse
# Custom modules/imports for this project
from web.forms import SettingsForm  # <--'SettingsForm' is the custom form to adjust signal parameters
from spectrum import Spectrum

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

def update_running_config(form):
    # Update the running config with form submission values
    global running_config

    # Frequency Range Settings
    running_config['frequency_range_start'] = form.frequency_range_start.data
    running_config['frequency_range_end'] = form.frequency_range_end.data
    running_config['frequency_range_num_points'] = form.frequency_range_num_points.data
    
    # Noise Floor Settings
    running_config['noise_floor_base_amplitude'] = form.noise_floor_base_amplitude.data
    running_config['noise_floor_high_energy_amplitude'] = form.noise_floor_high_energy_amplitude.data
    running_config['noise_floor_high_energy_frequency'] = form.noise_floor_high_energy_frequency.data
    running_config['noise_floor_low_energy_amplitude'] = form.noise_floor_low_energy_amplitude.data
    running_config['noise_floor_low_energy_frequency'] = form.noise_floor_low_energy_frequency.data
    
    # Signal Spike Settings
    spike_list = list(range(6))#list(form.)
    for i in spike_list:
        # This is gross, but at least it's compact. I don't want to talk about it.
        exec(f"running_config['signal_spike_{i}_amplitude'] = form.signal_spike_%d_amplitude.data" %i)
        exec(f"running_config['signal_spike_{i}_mu'] = form.signal_spike_%d_mu.data" %i)
        exec(f"running_config['signal_spike_{i}_sigma'] = form.signal_spike_%d_sigma.data" %i)

    generate_spectrum_animation(running_config)

def generate_spectrum_animation(config, filepath='web/static/', filename='spectrum_animation'): 

    global animation_filename
    animation_timestamp = datetime.now().strftime("%H%M%S")
    
    # Create instance of spectrum graph and plot it
    print("[+] Generating spectrum animation...")
    spectrum = Spectrum(config)
    spectrum.gen_animation().save(filepath + filename + '_' + animation_timestamp + '.gif', writer='pillow', fps=30)
    animation_filename = filename + '_' + animation_timestamp + '.gif'
    print("[+] Spectrum animation generated.")
    return spectrum, spectrum.gen_animation()

# Initialize the Flask App
app = Flask(__name__, template_folder='web/templates')
app.secret_key = '32wps'  # Flask requirement to enable CSRF protection as well as the 'flash' method functionality
app.config['SECRET_KEY'] = '32wps'  #something to do with CSRF, or something
args = parse_args()
running_config = load_config(args.config) # Initialize a global variable to store the running config
spectrum, spectrum_animation = generate_spectrum_animation(running_config)

# Initial root page. Renders the 'index.html' file showing an image of the Spectrum Analyzer
@app.route('/')
def index():
    return render_template('index.html', gif_filename = animation_filename)

# Settings modification page. Shows a form which is used to adjust the various signal parameters
@app.route('/settings', methods=['GET','POST'])
def settings():

    # Instantiate the form from the template
    form = SettingsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Update the running config with form submission values 
            update_running_config(form)
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('settings'))
        else:
            # Form validation failed
            print("Form validation failed!")
    
    # # Populate the Frequency Range fields with current config data
    form.frequency_range_start.default = running_config['frequency_range_start']
    form.frequency_range_end.default = running_config['frequency_range_end']
    form.frequency_range_num_points.default = running_config['frequency_range_num_points']
    
    # # Populate the Noise Floor fields with current config data
    form.noise_floor_base_amplitude.default = running_config['noise_floor_base_amplitude']
    form.noise_floor_high_energy_amplitude.default = running_config['noise_floor_high_energy_amplitude']
    form.noise_floor_high_energy_frequency.default = running_config['noise_floor_high_energy_frequency']
    form.noise_floor_low_energy_amplitude.default = running_config['noise_floor_low_energy_amplitude']
    form.noise_floor_low_energy_frequency.default = running_config['noise_floor_low_energy_frequency']
    
    # # Populate the Signal Spike fields with current config data
    spike_list = list(range(spectrum.count_spikes()))
    for i in spike_list:
        # This is gross, but at least it's compact. I don't want to talk about it.
        exec(f"form.signal_spike_%d_amplitude.default = running_config['signal_spike_{i}_amplitude']" %i)
        exec(f"form.signal_spike_%d_mu.default = running_config['signal_spike_{i}_mu']" %i)
        exec(f"form.signal_spike_%d_sigma.default = running_config['signal_spike_{i}_sigma']" %i)

    # Process the form with current config data
    form.process(obj=running_config)
    return render_template('settings.html', form=form)

# Static content page. Hosts images and other static content in case they need to be accessed directly.
@app.route('/static/<filename>')
def static_files(filename):
    # Serve static files (like the plot image) from the 'static' directory
    return send_from_directory('web/static', filename)

@app.route('/get_animation_filename')
def get_animation_filename():
    return jsonify({'gif_filename_latest': animation_filename})

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