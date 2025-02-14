# Compiler
CXX = g++
CXXFLAGS = -std=c++17 -Wall -I/opt/homebrew/Cellar/taglib/1.13.1/include

# Linker flags
LDFLAGS = -L/opt/homebrew/Cellar/taglib/1.13.1/lib -ltag -Wl,-rpath,/opt/homebrew/lib

# Target executable
TARGET = out
SRC = music.cpp

# Compile and link
$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

# Clean build files
clean:
	rm -f $(TARGET)
