#include "MySocket.h"
#include "errno.h"
#include <unistd.h>

#define MAX_BUFFER		1024

MySocket::MySocket(int port) {
	hSocket = 0;

   	while (!setup_server(port)) {
      	fprintf(stderr, "socket setup problem...exiting\n");
      	exit(1);
   	}
}

MySocket::~MySocket() {
    close(hSocket);
    close(hServerSocket);
}

// sets up a server side socket thingy
int MySocket::setup_server(int port) {
    puerta = port;
   	Address.sin_addr.s_addr = INADDR_ANY;
   	Address.sin_family      = AF_INET;
   	Address.sin_port        = htons(port);

   	printf("Creating SERVER socket...");
   	if ((hServerSocket = socket(AF_INET, SOCK_STREAM, 0)) == SOCKET_ERROR) {
    	printf("Could not create a SERVER socket...\n");
    	return 1;
   	}
   	else {
    	printf("OK\n");
   	}
   	//printf("Binding socket...\n");
   	if ((bind(hServerSocket, (struct sockaddr*)&Address, sizeof(Address))) == SOCKET_ERROR) {
    	printf("SERVER: Could not bind the SERVER socket...\n");
		printf("errno = %i\n", errno);
    	return 0;
   	}
   	//else {
    //	printf("OK\n");
   	//}

   	//Listening queue
   	listen(hServerSocket, QUEUE_SIZE);

   	return 1;
}

void MySocket::AcceptEm() {
   	printf("SERVER: Waiting for connection (%i) ... ", puerta);
	//printf("errno = %i\n", errno);
	unsigned int junk = sizeof(Address);
   	hSocket = accept(hServerSocket, (struct sockaddr*)&Address, &junk); //(unsigned int*)junk);
	//printf("errno = %i\n", errno);
	//printf("hSocket = %i\n", hSocket);
   	printf("SERVER: Connection received\n");
}


int MySocket::SendMessage(char *message, int len) {
	int bsent = 0;
    
    //printf("Sent: %s\n", message);

	//printf("message sending: %s, socket = %i\n", message, m_hSocket);
	if ((bsent = send(hSocket, message, len, 0)) == SOCKET_ERROR) {
		printf("SERVER: error sending socket message: %s\n", message);
		//close(hServerSocket);
		//close(m_hSocket);
		//exit(0);
	}
	//printf("bsent = %i\n", bsent);

	return 1;
}

int MySocket::ReadMessage(char *message) {
	memset(message, 0, MAX_BUFFER);

	//printf("to do recv in ReadMessage\n");
	int NumBytes = recv(hSocket, message, MAX_BUFFER, 0);

	if (NumBytes == SOCKET_ERROR) {
		fprintf(stderr,"errno = %i\n", errno);
		fprintf(stderr,"EBADF = %i\n", EBADF);
		fprintf(stderr,"ECONNREFUSED = %i\n", ECONNREFUSED);
		fprintf(stderr,"ENOTCONN = %i\n", ENOTCONN);
		fprintf(stderr,"ENOTSOCK = %i\n", ENOTSOCK);
		fprintf(stderr,"if not found, check man page\n");
		fprintf(stderr,"Socket Error reading message: %i\n", NumBytes);
		exit(1);
		//close(m_hSocket);
		//close(hServerSocket);
		//throw "Error Reading From Socket";
	}

	return NumBytes;
}
