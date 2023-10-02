import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from spectrum import spectrum  # Import your Spectrum class

class ConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('config.yaml'):
            print("Config file changed. Regenerating graph...")
            spectrum_analyzer = spectrum('config/config.yaml')
            spectrum_analyzer.plot_spectrum_graph()

if __name__ == "__main__":
    event_handler = ConfigHandler()
    observer = Observer()
    observer.schedule(event_handler, path='config', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
