from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import InputRequired

class SignalSpikeForm(FlaskForm):
    # Signal Spike Params
    signal_spike_amplitude = FloatField('Signal Spike Amplitude', validators=[InputRequired()])
    signal_spike_mu = FloatField('Signal Spike Center Frequency (mu)', validators=[InputRequired()])
    signal_spike_sigma = FloatField('Signal Spike Width (sigma)', validators=[InputRequired()])


class SettingsForm(FlaskForm):
    # Frequency Range Params
    frequency_range_start = FloatField('Frequency Range Start', validators=[InputRequired()])
    frequency_range_end = FloatField('Frequency Range End', validators=[InputRequired()])
    num_points = IntegerField('Number of Points to Plot', validators=[InputRequired()])
    
    # Noise Floor Params 
    noise_floor_base_amplitude = FloatField('Noise Floor Base Amplitude', validators=[InputRequired()])
    noise_floor_high_energy_amplitude = FloatField('Noise Floor High Energy Amplitude', validators=[InputRequired()])
    noise_floor_high_energy_frequency = FloatField('Noise Floor High Energy Frequency', validators=[InputRequired()])
    noise_floor_low_energy_amplitude = FloatField('Noise Floor Low Energy Amplitude', validators=[InputRequired()])
    noise_floor_low_energy_frequency = FloatField('Noise Floor Low Energy Frequency', validators=[InputRequired()])

    # Zero to ten sets of signal spike parameters
    signal_spike_params = FieldList(FormField(SignalSpikeForm), max_entries=10)
    
    # Submit Form
    submit = SubmitField('Update Settings')
