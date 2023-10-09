# Still to do: 
### Overall
- ensure that the ffmpeg library gets installed on destination machine
- package everything up for export offline
- update this to be an actual readme

### Spectrum.py
- make line points convolve, rather than superimpose


### App.py
- make the regen of the animation clean up old animations
- put the app.py functions in an app.py class? Make an app.py config? 
- make update_running_config count signal spikes properly

### Index.html
- Make background color dark grey
- center animation on page

### Settings.html
- make background color dark grey
- add inject buttons to simulate different scenarios
- add functionality to add or remove spikes on the /settings page


# Done
- Make form default values match the current running config
- make form submission update the .gif of the spectrum
- Change line color to yellow or green, and thinner
- change plot background to black with grey grid lines
- add axes labels
- resize animation to be most of a 1080 screen width
- extend boundaries of the line that is computed out about 10 points at both ends to make it animate off-screen
- tune number of frames to ensure the animation always starts and ends off-screen
- add axes labels at the center frequency of each spike