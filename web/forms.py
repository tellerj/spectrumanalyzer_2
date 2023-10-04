from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import InputRequired

class SettingsForm(FlaskForm):
    # Frequency Range Params
    frequency_range_start = IntegerField('Frequency Range Start', validators=[InputRequired()], default=2500)
    frequency_range_end = IntegerField('Frequency Range End', validators=[InputRequired()], default=7500)
    frequency_range_num_points = IntegerField('Number of Points to Plot', validators=[InputRequired()], default=1000)
    
    # Noise Floor Params 
    noise_floor_base_amplitude = FloatField('Noise Floor Base Amplitude', validators=[InputRequired()], default=10.0)
    noise_floor_high_energy_amplitude = FloatField('Noise Floor High Energy Amplitude', validators=[InputRequired()], default=2.0)
    noise_floor_high_energy_frequency = FloatField('Noise Floor High Energy Frequency', validators=[InputRequired()], default=1000.0)
    noise_floor_low_energy_amplitude = FloatField('Noise Floor Low Energy Amplitude', validators=[InputRequired()], default=1.0)
    noise_floor_low_energy_frequency = FloatField('Noise Floor Low Energy Frequency', validators=[InputRequired()], default=0.01)

    # Signal Spike Params
    signal_spike_0_amplitude = FloatField('Signal Spike Alpha - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_0_mu = FloatField('Signal Spike Alpha - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_0_sigma = FloatField('Signal Spike Alpha - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_1_amplitude = FloatField('Signal Spike Beta - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_1_mu = FloatField('Signal Spike Beta - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_1_sigma = FloatField('Signal Spike Beta - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_2_amplitude = FloatField('Signal Spike Charlie - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_2_mu = FloatField('Signal Spike Charlie - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_2_sigma = FloatField('Signal Spike Charlie - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_3_amplitude = FloatField('Signal Spike Delta - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_3_mu = FloatField('Signal Spike Delta - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_3_sigma = FloatField('Signal Spike Delta - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_4_amplitude = FloatField('Signal Spike Echo - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_4_mu = FloatField('Signal Spike Echo - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_4_sigma = FloatField('Signal Spike Echo - Sigma (Width)',validators=[InputRequired()], default=0.0)

    signal_spike_5_amplitude = FloatField('Signal Spike Fox - Amplitude',validators=[InputRequired()], default=0.0)
    signal_spike_5_mu = FloatField('Signal Spike Fox - Mu (Center Frequency)',validators=[InputRequired()], default=0.0)
    signal_spike_5_sigma = FloatField('Signal Spike Fox - Sigma (Width)',validators=[InputRequired()], default=0.0)
    
    # Submit Form
    submit = SubmitField('Update Settings')
