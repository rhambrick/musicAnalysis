#include <fstream>
#include <iostream>
#include <filesystem>
#include <bits/stdc++.h>
using namespace std;
namespace fs = filesystem;

int main()
{
    // Scan for .flac and .mp3's in USB drive's Music folder (change path if needed, or file paths for flexibility)
    string path("D:\\Music");
    string flac(".flac");
    string mp3(".mp3");

    // Create a vector (dynamic array) of filenames
    vector<string> filenames;

    //Loop through all sub-folders of Music and add files with that extnetion to the vector
    for (auto &p : fs::recursive_directory_iterator(path))
    {
        if (p.path().extension() == flac || p.path().extension() == mp3)
            filenames.push_back(p.path().string());
    }

    // Print out these filenames for debugging as of now
    for(auto i : filenames)
        cout << i << " \n";
    
    return 0;
}