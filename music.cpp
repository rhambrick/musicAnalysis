// clang++ music.cpp -o out -std=c++17 -stdlib=libc++ -I/opt/homebrew/Cellar/taglib/1.13.1/include -L/opt/homebrew/Cellar/taglib/1.13.1/lib -ltag 
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
    int index;
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
    string path;
    cout << "Enter the top folder path to scan: ";
    getline(cin, path);

    string flac = ".flac";
    string mp3 = ".mp3";
    string wav = ".wav";

    // Vector of song structs
    vector<Song> list;

    //Loop through all sub-folders of Music and add files with that extension to the vector
    int index = 0;
    for (auto& item : fs::recursive_directory_iterator(path))   // recursively loop through all sub-folders
    {
        if (item.path().extension() == flac || item.path().extension() == mp3 || item.path().extension() == wav) {    // if item is a song

            TagLib::FileRef file(item.path().c_str());  // initalize taglib for the current file's path as a string (from the docs)

            cout << index << " Title: " << file.tag()->title() << endl;
            cout << "Album:" << file.tag()->album() << endl;
            cout << "Genre:" << file.tag()->genre() << endl;
            cout << endl;

            index++;
        }
    }
    
    return 0;
}
