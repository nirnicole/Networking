#include <stdio.h>
//#include <sys/socket.h>
//#include <arpa/inet.h>
//#include <unistd.h>
#include <string.h>
#include <winsock.h>   //take off
#include <WS2tcpip.h>	//take off
#include <exception>
#include <iostream>

//#define DEST "119.4.7.5";
//#define PORT 8080;

int main(int argc, char const* argv[])
{
	try {
		char address[] = "119.4.7.5";
		int port = 8080;

		int sock = 0, valread, i;
		struct sockaddr_in serv_addr;
		char msg1[] = "Good morning server\n ";
		char msg2[] = "Nice to see you\n";
		char buffer[129] = { 0 };

		if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
			printf("\nSocket creation error\n");
			return 1;
		}
		serv_addr.sin_family = AF_INET;
		serv_addr.sin_port = htons(port);

		if (inet_pton(AF_INET, address, &serv_addr.sin_addr) <= 0) {
			printf("\nInvalid address\nAddress not supported\n");
			return 1;
		}

		if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
			printf("\nConnection Failed\n");
			return -1;
		}

		send(sock, msg1, strlen(msg1), 0);
		send(sock, msg2, strlen(msg2), 0);
		printf("Hello message sent\n");

		//valread = read(sock, buffer, 1024);
		for (i = 0; i < 128; i++) {
			if (buffer[i] == '\n') {
				buffer[i + 1] = '\0';
				break;
			}
		}

		if (i == 128)
			printf("%s\n", buffer);
	}
	catch (const std::exception& e) {
		std::cout << e.what() << '\n';
	}
	return 0; 
}
