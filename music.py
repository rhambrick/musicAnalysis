import essentia.standard as es
from mutagen.mp3 import MP3
import os

# Function to analyze BPM and Key
def analyze_audio(file_path):
    try:
        # Load audio file using Essentia
        loader = es.MonoLoader(filename=file_path)
        audio = loader()

        # Compute tempo (BPM)
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, _, _, _, _ = rhythm_extractor(audio)

        # Compute key
        key_extractor = es.KeyExtractor()
        key, scale, strength = key_extractor(audio)

        return bpm, f"{key} {scale}"
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

# Function to scan folders recursively
def scan_music_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mp3", ".flac", ".wav")):
                file_path = os.path.join(root, file)
                bpm, key = analyze_audio(file_path)
                
                if bpm and key:
                    print(f"🎵 {file} | BPM: {bpm} | Key: {key}")

# Ask user for folder input
folder_path = input("Enter the top folder path to scan: ")
scan_music_folder(folder_path)
