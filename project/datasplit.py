import os
import pandas as pd

def split_dataset(dataset_path, raw_data_folder, num_files):
    # Load the dataset
    dataset = pd.read_csv(dataset_path)

    # Create the raw-data folder if it doesn't exist
    if not os.path.exists(raw_data_folder):
        os.makedirs(raw_data_folder)

    # Split the dataset into chunks of 10 rows each
    chunks = [dataset[i:i+30] for i in range(0, len(dataset), 30)]

    # Save each chunk as a separate file
    for i in range(num_files):
        chunk = chunks[i % len(chunks)]  # Use modulo to cycle through the chunks
        chunk.to_csv(os.path.join(raw_data_folder, f'file_{i+1}.csv'), index=False)

if __name__ == "__main__":
    dataset_path = 'G:/dsp_projectds/Clean_Dataset.csv'  # Change this to the path of your dataset
    raw_data_folder = 'C:/Users/AbdulHanan/dsp-abdulhananbin-saeed/raw-data'  # Change this to the desired raw-data folder path
    num_files = 30154  # Change this to the desired number of files to generate
    
    split_dataset(dataset_path, raw_data_folder, num_files)
