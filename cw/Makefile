CC=g++
CFLAGS=-std=c++14 -c
OUTPUT = cw
GLEWLIB = -lGL -lGLEW -lglfw

all: cw

cw: main.o object.o matrix.o shaders.o
	$(CC) main.o object.o matrix.o shaders.o $(GLEWLIB) -o $(OUTPUT)

main.o: main.cpp
	$(CC) $(CFLAGS) main.cpp

object.o: object.cpp
	$(CC) $(CFLAGS) object.cpp

matrix.o: matrix.cpp
	$(CC) $(CFLAGS) matrix.cpp

shaders.o: shaders.cpp
	$(CC) $(CFLAGS) shaders.cpp

clean:
	rm -rf *.o $(OUTPUT)