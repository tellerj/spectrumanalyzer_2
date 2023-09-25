from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import InputRequired

# class SignalSpikeForm(FlaskForm):
#     # Signal Spike Params
#     signal_spike_amplitude = FloatField('Signal Spike Amplitude', validators=[InputRequired()],default=0.0)
#     signal_spike_mu = FloatField('Signal Spike Center Frequency (mu)', validators=[InputRequired()],default=0.0)
#     signal_spike_sigma = FloatField('Signal Spike Width (sigma)', validators=[InputRequired()],default=0.0)


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

    # Signal Spike Params
    signal_spike_alpha_amplitude = FloatField('Signal Spike Alpha - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_alpha_mu = FloatField('Signal Spike Alpha - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_alpha_sigma = FloatField('Signal Spike Alpha - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_beta_amplitude = FloatField('Signal Spike Beta - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_beta_mu = FloatField('Signal Spike Beta - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_beta_sigma = FloatField('Signal Spike Beta - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_charlie_amplitude = FloatField('Signal Spike Charlie - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_charlie_mu = FloatField('Signal Spike Charlie - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_charlie_sigma = FloatField('Signal Spike Charlie - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_delta_amplitude = FloatField('Signal Spike Delta - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_delta_mu = FloatField('Signal Spike Delta - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_delta_sigma = FloatField('Signal Spike Delta - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_echo_amplitude = FloatField('Signal Spike Echo - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_echo_mu = FloatField('Signal Spike Echo - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_echo_sigma = FloatField('Signal Spike Echo - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_fox_amplitude = FloatField('Signal Spike Fox - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_fox_mu = FloatField('Signal Spike Fox - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_fox_sigma = FloatField('Signal Spike Fox - Sigma (Width)',validators=[InputRequired()], default=0.0)
    
    # Submit Form
    submit = SubmitField('Update Settings')
