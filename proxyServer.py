"""
Concept:
        Client -> ProxyServer -> Server
        Client <- ProxyServer <- Server

        1. the client connects to the proxy(as a web server).
        2. the proxy listens in an infinite loop until thers a request from client.
        3. the proxy than calls handle_client which extract the data from the client and sends it to the real server.
        4. the server returns answer that goes back to the client through the proxy.

 -  this proxy also changes the data it gets from the client,
    specificly the host name so it redirects the client to NEW_HOST site.

 -  NOTE: no basic securities defences were apllyed on this proxy server, so it's flow will be clear as possible.
"""

import socket
import re
import threading

HOST = 'localhost'              # The server's hostname or IP address '127.0.0.1'
PORT = 80                       # Can be replaced to any port, recomended a higer one.
NEW_HOST = 'www.example.com'    # New host target. (you can change to any site..)

#a function to execute the delivery of the manipulated data to the server
def toServer(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((NEW_HOST,PORT))
    print("sending data to server:\t", data)
    s.send(data)
    return s.recv(4096)

#stream the data from the client to the server - but also manipulate it here(in this case we enforcing a different host request)
def HandleClient(conn):
    with conn:
        #take the data sent from the client
        data = conn.recv(4096)

        #manipulate the data (change host target request, you can add another maniplations here)
        temp = data.decode('utf-8')
        newdata = temp
        newdata = re.sub(r'Host.*\r', "Host: " + NEW_HOST + "\r", temp).encode('utf-8')

        #pass the manipulated data to the server
        res = toServer(newdata)
        conn.sendall(res)

#proxy server (acts like a web server!)
"""
flow:
    1. socket - create a socket.
    2. bind - bind the host and the port together within the socket.
    3. listen - listen on the socket for client requests for connection.
    4. infinite loop:
    4.1             accept - if a client request to connect accept his connection and take the socket fd and adress
(*) 4.2             handle - handle the client with a specific agenda, manipulate his data and pass it to the server.

"""
def proxy(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        while True:
            conn, address = sock.accept()
            print("connection from:\t", address)

            # Thread the client, unprotected multithreading
            # we should limit amount of threads and maybe lock resorces if we will add any to the manipulation procces.
            threading.Thread(target=HandleClient, args=(conn,)).start()
            #HandleClient(conn)


if __name__ == '__main__':
    print("proxy is running...")
    proxy(HOST, PORT)