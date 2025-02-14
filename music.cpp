// clang music.cpp -o out.app -std=c++17 -I/opt/homebrew/Cellar/taglib/1.13.1/include -L/opt/homebrew/Cellar/taglib/1.13.1/lib -ltag 
#include <fstream>
#include <string>
#include <iostream>
#include <filesystem>
#include <taglib/fileref.h>
#include <taglib/tag.h>

using namespace std;
namespace fs = filesystem;

// Structure of each song
struct Song {
    int number;
    string name;
    string artist;
    string album;
    string genre;
    int tempo;
    string key;
    string score;
};

int main()
{
    // Scan for .flac and .mp3's in USB drive's Music folder (change path if needed, or file paths for flexibility) currently configured for my mac
    string path("/Volumes/REAGAN32/Music");
    string flac(".flac");
    string mp3(".mp3");

    // Vector of song structs
    vector<Song> list;

    //Loop through all sub-folders of Music and add files with that extension to the vector
    int index = 0;
    for (const auto & item : fs::recursive_directory_iterator(path))
    {
        if (item.path().extension() == flac || item.path().extension() == mp3)
            // Extract metadata
            TagLib::FileRef file(item.path().c_str());

            // Create a Song struct and fill it with the extracted metadata
            Song song;
            song.number = index;
            song.name = file.tag() && !file.tag()->title().isEmpty() ? file.tag()->title().to8Bit(true) : "Unknown Title";
            song.artist = file.tag() && !file.tag()->artist().isEmpty() ? file.tag()->artist().to8Bit(true) : "Unknown Artist";
            song.album = file.tag() && !file.tag()->album().isEmpty() ? file.tag()->album().to8Bit(true) : "Unknown Album";
            song.genre = file.tag() && !file.tag()->genre().isEmpty() ? file.tag()->genre().to8Bit(true) : "Unknown Genre";

            // Push the song struct into the vector
            list.push_back(song);

            // Print the extracted song information, for debugging for now
            cout << index << " - " << song.name << " - " << song.artist << " - " << song.genre << endl;

            index++;
    }
    
    return 0;
}