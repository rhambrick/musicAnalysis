#include <iostream>
#include <taglib/fileref.h>
#include <taglib/tag.h>

using namespace std;

int main() {
    TagLib::FileRef file("/Users/reagan/Music/Songs to Spin/losing my mind/07 HOT TO GO!.mp3");
        cout << "Title: " << file.tag()->title() << endl;
        cout << "Album:" << file.tag()->album() << endl;
        cout << "Genre:" << file.tag()->genre() << endl;
    return 0;
}