from spectrum import spectrum

def main():
    # Point to config file
    config_file = 'config.yaml'

    # Create instance of spectrum graph
    spectrum_analyzer = spectrum(config_file)

    # Generate and display spectrum plot
    spectrum_analyzer.plot_spectrum_graph()

if __name__ == "__main__":
    main()