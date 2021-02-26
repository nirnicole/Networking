#include <boost/asio.hpp>
#include <iostream>
#include <exception>

using boost::asio::ip::tcp;

int main() {

	char address[] = "119.4.7.5";	
	char port[] = "8080";
	
	try {
		boost::asio::io_context io_context;
		tcp::socket s(io_context);
		tcp::resolver resolver(io_context);
	
		boost::asio::connect(s, resolver, resolver.resolve(address, port));
	
		const int max_Length = 129;
		char request1[] = "Good morning server";
		char request2[] = "Nice to see you";
		char data[max_Length];
		boost::asio::write(s, boost::asio::buffer(request1, strlen(request1)));
		boost::asio::write(s, boost::asio::buffer(request2, strlen(request2)));
	
		boost::asio::read(s, boost::asio::buffer(data, max_Length));
		for (int i = 0; i < 128; i++) {
			if (data[i] == '\n') {
				data[i + 1] = '\0';
				break;
			}
			std::cout << "Received: " << data << std::endl;
		}
	}
	catch(const std::exception& e) {
			std::cout << e.what() << '\n';
	}

	return 0;
}