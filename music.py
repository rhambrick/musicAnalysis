import essentia.standard as es  # Essentia for key and tempo
from mutagen.easyid3 import EasyID3  # Mutagen for audio file metadata
import os
import csv
import pandas as pd  # Pandas for csv work

CSV_FILE = "songData.csv"  # Store scanned data here

# Function to analyze BPM and Key
def analyze_audio(file_path):
    loader = es.MonoLoader(filename=file_path)
    audio = loader()

    # Compute tempo (BPM)
    rhythm_extractor = es.RhythmExtractor2013()
    bpm, _, _, _, _ = rhythm_extractor(audio)

    # Compute key
    key_extractor = es.KeyExtractor()
    key, scale, strength = key_extractor(audio)

    return bpm, f"{key} {scale}"

# Function to extract metadata (title, artist, genre)
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)  # Read metadata
        title = audio.get("title", [os.path.basename(file_path)])[0]  # Default to filename if missing
        artist = audio.get("artist", ["Unknown"])[0]
        genre = audio.get("genre", ["Unknown"])[0]
        return title, artist, genre
    except Exception:
        return os.path.basename(file_path), "Unknown", "Unknown"  # Default values

# Load existing CSV data
def load_existing_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return set(df["Song Name"])  # Convert column to set for O(1) lookups
    return set()

# Function to scan folders and update CSV after each file
def scan_music_folder(folder_path):
    scanned_files = load_existing_data()
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        
        # Write header if the CSV is empty
        if not file_exists or os.stat(CSV_FILE).st_size == 0:
            writer.writerow(["Index", "Song Name", "Artist", "BPM", "Key", "Genre"])  

        index = len(scanned_files) + 1  # Start indexing at 1

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".flac", ".wav")):
                    file_path = os.path.join(root, file)
                    
                    title, artist, genre = get_metadata(file_path)

                    if title in scanned_files:
                        continue  # Skip duplicate songs
                    
                    bpm, key = analyze_audio(file_path)
                    
                    if bpm and key:
                        writer.writerow([index, title, artist, bpm, key, genre])  # Write each result as they come in
                        print(f"✅ Scanned: {title} | BPM: {bpm} | Key: {key}")
                        scanned_files.add(title)
                        index += 1

# Function to display sorted results
def display_sorted_results():
    df = pd.read_csv(CSV_FILE)
    df = df.sort_values(by="BPM", ascending=True)  # Sort by BPM
    print(df.to_string(index=False))  # Print neatly

# Run the program
folder_path = input("Enter the top folder path to scan: ")
scan_music_folder(folder_path)
print("\n📊 Sorted Results (by BPM):")
display_sorted_results()
