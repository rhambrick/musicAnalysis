import essentia.standard as es  # for key and bpm algos
from mutagen.easyid3 import EasyID3 # for audio metadata
import os
import csv
import pandas as pd # for csv work

CSV_FILE = "songData.csv"  # store scanned data here: index, song, artist, key, bpm, genre (if there)

# function to analyze bpm and key
def analyze_audio(file_path):
    try:
        loader = es.MonoLoader(filename=file_path)
        audio = loader()

        # get tempo
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, _, _, _, _ = rhythm_extractor(audio)

        # get key
        key_extractor = es.KeyExtractor()
        key, scale, strength = key_extractor(audio)

        return bpm, f"{key} {scale}"
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

# function to extract metadata (artist, genre)
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)  # read all metadata
        artist = audio.get("artist", ["Unknown"])[0]
        genre = audio.get("genre", ["Unknown"])[0]
        return artist, genre
    except Exception:
        return "Unknown", "Unknown"

# load existing CSV data to skip already scanned files for speed
def load_existing_data():
    if not os.path.exists(CSV_FILE):
        return set()
    
    scanned_files = set()
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if row:  
                scanned_files.add(row[1])  # store song names
    return scanned_files

# function to scan folders and store results
def scan_music_folder(folder_path):
    scanned_files = load_existing_data()
    new_data = []
    index = len(scanned_files) + 1

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mp3", ".flac", ".wav")) and file not in scanned_files:
                file_path = os.path.join(root, file)
                
                bpm, key = analyze_audio(file_path)
                artist, genre = get_metadata(file_path)
                
                if bpm and key:
                    new_data.append([index, file, artist, bpm, key, genre])
                    print(f"✅ Scanned: {file} | BPM: {bpm} | Key: {key}")
                    index += 1

    # save new results
    if new_data:
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            if os.stat(CSV_FILE).st_size == 0:
                writer.writerow(["Index", "Song Name", "Artist", "BPM", "Key", "Genre"])  # write header if empty
            writer.writerows(new_data)

# function to display sorted results
def display_sorted_results():
    if not os.path.exists(CSV_FILE):
        print("No songs scanned yet!")
        return

    df = pd.read_csv(CSV_FILE)
    df = df.sort_values(by="BPM", ascending=True)  # sort by BPM
    print(df.to_string(index=False))  # print neatly

# run the program
folder_path = input("Enter the top folder path to scan: ")
scan_music_folder(folder_path)
print("\n📊 Sorted Results (by BPM):")
display_sorted_results()
