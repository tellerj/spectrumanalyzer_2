from flask import Flask, render_template, send_from_directory
from spectrum import spectrum

app = Flask(__name__, template_folder='web/templates')

@app.route('/')
def index():
    
    # Create instance of spectrum graph and plot it
    spectrum_analyzer = spectrum('config/config.yaml')
    spectrum_analyzer.plot_spectrum_graph()

    return render_template('index.html')

@app.route('/static/<filename>')
def static_files(filename):
    # Serve static files (like the plot image) from the 'static' directory
    return send_from_directory('web/static', filename)

if __name__ == "__main__":
    app.run(debug=True)