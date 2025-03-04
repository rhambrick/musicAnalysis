// clang++ essentiaTest.cpp -o test -std=c++17 -I/opt/homebrew/include -L/opt/homebrew/lib -lessentia -lfftw3 -lstdc++

#include <iostream>
#include <essentia/essentia.h>
#include <essentia/algorithmfactory.h>

int main() {
    essentia::init();
    std::cout << "Essentia initialized successfully!" << std::endl;
    essentia::shutdown();
    return 0;
}