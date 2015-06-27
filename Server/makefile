PROGRAM = CheapTalk
cpp_FILES = main.cpp MySocket.cpp
c_FILES =
CC = g++

CFLAGS = -O -g
LIBs = 

OBJECTS = $(c_FILES:.c=.o) $(cpp_FILES:.cpp=.o)

.SUFFIXES: .o .cpp .c

.cpp.o:
	$(CC) $(FLAGS) $(CFLAGS) $< -c $(INCLUDES)

.c.o:
	$(CC) $(FLAGS) $(CFLAGS) $< -c $(INCLUDES)

$(PROGRAM): $(OBJECTS)
	$(CC) $(FLAGS) $(CFLAGS) -o $@ $(INCLUDES) $(OBJECTS) $(LIBS)

clean:
	rm *.o

rebuild: clean
	make
