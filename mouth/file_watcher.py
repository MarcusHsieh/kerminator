import os
import time
import json

# watching this dir
watch_dir = "/home/kermie/incoming_files"

def process_file(file_path):
    print(f"Processing file: {file_path}")
    with open(file_path, "r") as f:
        data = json.load(f)
        # process the JSON data (move servos based on RMS amplitude array)
        print(data)  # REPLACE THIS WITH YOUR CODE TO MOVE SERVOS
    os.remove(file_path)  # remove file after processing
    

def watch_directory(directory):
    processed_files = set()  # track processed files
    while True:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith(".json") and file_path not in processed_files:
                process_file(file_path)
                processed_files.add(file_path)
        time.sleep(0.5)  # check for new files every half second (maybe 1 second okay)

if __name__ == "__main__":
    if not os.path.exists(watch_dir):
        os.makedirs(watch_dir)
    print(f"Watching directory: {watch_dir}")
    watch_directory(watch_dir)
