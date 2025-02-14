// clang++ -std=c++17 -I/opt/homebrew/include -L/opt/homebrew/lib -ltag test.cpp -o test

#include <iostream>
#include <taglib/fileref.h>
#include <taglib/tag.h>

using namespace std;

int main() {
    TagLib::FileRef file("/Users/reagan/Music/Songs to Spin/losing my mind/07 HOT TO GO!.mp3");
    if (!file.isNull() && file.tag()) {
        cout << "Title: " << file.tag()->title().to8Bit(true) << endl;
    } else {
        cout << "Could not read metadata." << endl;
    }
    return 0;
}
