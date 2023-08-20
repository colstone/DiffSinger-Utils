import os
import time
from tqdm import tqdm  # Import the progress bar library

def convert_time_to_frames(time_str):
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    frames = int((hours * 3600 + minutes * 60 + seconds) * 10000000)  # Convert to 100ns units (HTK format)
    return frames

def convert_to_htk_lab(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    htk_lab_lines = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 3:
            start_time = convert_time_to_frames(parts[1])
            end_time = convert_time_to_frames(parts[2])
            label = parts[0]
            htk_lab_lines.append(f"{start_time} {end_time} {label}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(htk_lab_lines))

def batch_convert_folder(input_folder):
    for root, _, files in os.walk(input_folder):
        for filename in tqdm(files, desc="Converting files", unit="file"):
            if filename.endswith(".txt"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(root, filename.replace(".txt", ".lab"))
                convert_to_htk_lab(input_path, output_path)
                time.sleep(0.55)  # Add a delay of 0.55 seconds between conversions

def main():
    batch_mode = input("Do you want to enable batch conversion? (y/n): ")
    
    if batch_mode.lower() == 'y':
        input_folder = input("Enter the folder path: ")
        batch_convert_folder(input_folder)
        print("Batch conversion completed.")
    else:
        input_filename = input("Enter the input txt file path: ")
        output_filename = input_filename.replace(".txt", ".lab")
        convert_to_htk_lab(input_filename, output_filename)
        print(f"Conversion completed. Output file: {output_filename}")

if __name__ == "__main__":
    main()