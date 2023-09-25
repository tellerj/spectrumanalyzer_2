from flask import Flask, render_template, send_from_directory
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

    if 'add_signal_spike' in request.form

    # Run when the form is submitted, and passes the built-in validation check
    if form.validate_on_submit():
        # Update config with form data
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
                    'amplitude' : form.signal_spike_amplitude.data,
                    'mu' : form.signal_spike_mu.data,
                    'sigma' : form.signal_spike_sigma.data
                }
            ]
        }

        # Save updated configuration to the config file
        with open('config/config.yaml', 'w') as f:
            yaml.dump(config, f)

        return app.redirect(app.url_for('index'))
    
    # Open the current config to populate the form
    with open('config/config.yaml', 'r') as f:
        current_config = yaml.load(f, Loader=yaml.FullLoader)

    # # Populate the Frequency Range fields with current config data
    # form.frequency_range_start.default = current_config['frequency_range']['start']
    # form.frequency_range_end.default = current_config['frequency_range']['end']
    # form.num_points.default = current_config['frequency_range']['num_points']
    # # Populate the Noise Floor fields with current config data
    # form.noise_floor_base_amplitude.default = current_config['noise_floor_params']['base_amplitude']
    # form.noise_floor_high_energy_amplitude.default = current_config['noise_floor_params']['high_energy_amplitude']
    # form.noise_floor_high_energy_frequency.default = current_config['noise_floor_params']['high_energy_frequency']
    # form.noise_floor_low_energy_amplitude.default = current_config['noise_floor_params']['low_energy_amplitude']
    # form.noise_floor_low_energy_frequency = current_config['noise_floor_params']['low_energy_frequency']
    # # Populate the Signal Spike fields with current config data
    # form.signal_spike_amplitude = int(current_config['signal_spike_params']['amplitude'])
    # form.signal_spike_mu = int(current_config['signal_spike_params']['mu'])
    # form.signal_spike_sigma = int(current_config['signal_spike_params']['sigma'])

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