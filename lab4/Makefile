CC=g++
CFLAGS=-std=c++14 -c
OUTPUT = result

all: result

result: main.o object.o matrix.o shaders.o generators.o
	$(CC) main.o object.o matrix.o shaders.o generators.o -lGL -lGLEW -lglfw -Wall -Wextra -o $(OUTPUT)

main.o: main.cpp
	$(CC) $(CFLAGS) main.cpp

object.o: object.cpp
	$(CC) $(CFLAGS) object.cpp

matrix.o: matrix.cpp
	$(CC) $(CFLAGS) matrix.cpp

shaders.o: shaders.cpp
	$(CC) $(CFLAGS) shaders.cpp

generators.o: generators.cpp
	$(CC) $(CFLAGS) generators.cpp

clean:
	rm -rf *.o $(OUTPUT)