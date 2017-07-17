CXX=g++

CFLAGS   = -std=c99   -Wall -Wextra 
CXXFLAGS = -std=c++11 -Wall -Wextra 
DBGFLAGS = -g3 -DDEBUG -fsanitize=memory,undefined,integer -fsanitize-recover=all 
RELFLAGS = -Os -DNDEBUG -fPIE -fno-stack-protector -z execstack #-s

.DEFAULT_GOAL := all

.PHONY: all
all: CFLAGS   += $(RELFLAGS)
all: CXXFLAGS += $(RELFLAGS)
all: primecoder

primecoder: primecoder.cpp 
	$(CXX) -o $@ $^ $(CXXFLAGS) #-g3

.PHONY: clean
clean:
	rm -f primecoder
