# INSTRUCTIONS
# Create a virtual environment using command 'python -m venv venv'
# Activate virtual environment 'venv/scripts/activate'
# Install dependencies 'pip install -r requirements.txt'
# Run script 'python bgremove.py' in virtual environment


import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rembg import remove

# Set your source (Downloads) and destination directories
SOURCE_DIR = r'C:\Users\Personal\Downloads'  # The folder to watch
DEST_DIR = r'C:\2025\simple-project-two\reyes\cashier\img\products\starter'  # output folder

# List of allowed image file extensions
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Log event details for debugging
        print(f"[DEBUG] on_created event: {event.src_path}")
        if not event.is_directory:
            self.check_and_process(event.src_path)
    
    def on_modified(self, event):
        # Log event details for debugging
        print(f"[DEBUG] on_modified event: {event.src_path}")
        if not event.is_directory:
            self.check_and_process(event.src_path)
    
    def check_and_process(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            try:
                # Get initial size and wait to see if the file is fully written
                initial_size = os.path.getsize(filepath)
                time.sleep(1)
                current_size = os.path.getsize(filepath)
                if initial_size != current_size:
                    print(f"[INFO] File {filepath} is still being written. Skipping processing for now.")
                    return
                # Process the image
                self.process_image(filepath)
            except Exception as e:
                print(f"[ERROR] Error checking file {filepath}: {e}")
    
    def process_image(self, filepath):
        try:
            # Read the image in binary mode
            with open(filepath, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove the background
            output_data = remove(input_data)
            
            # Create output filename (always save as PNG to preserve transparency)
            base_name = os.path.basename(filepath)
            name_without_ext = os.path.splitext(base_name)[0]
            output_filename = os.path.join(DEST_DIR, f"{name_without_ext}.png")
            
            # Write the processed image to the destination folder
            with open(output_filename, 'wb') as output_file:
                output_file.write(output_data)
            
            print(f"[SUCCESS] Processed image saved as: {output_filename}")
        except Exception as e:
            print(f"[ERROR] Error processing {filepath}: {e}")

if __name__ == "__main__":
    # Ensure the destination directory exists
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()
    
    print(f"Monitoring folder: {SOURCE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()
    observer.join()
