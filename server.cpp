#include <boost/asio.hpp>
#include <iostream>
using boost::asio::ip::tcp;

int main() {
	
	try{
		const int MAX_LENGTH = 1024;
		int port = 1234;
		boost::asio::io_context io_context;

		tcp::acceptor a(io_context, tcp::endpoint(tcp::v4(), port));
		tcp::socket sock = a.accept();

		char data[MAX_LENGTH];
		size_t length = boost::asio::read(sock, boost::asio::buffer(data, MAX_LENGTH));
		std::cout << "Message in:\t" <<  data;
	}
	catch (const std::exception& e) {
		std::cout << e.what() << '\n';
	}

	return 0;
}