import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address    '119.4.7.5'
PORT = 8080        # The port used by the server
FORMAT = "utf-8"

try:
    f = open("message.txt")
    msg = f.read().encode(FORMAT)
    f.close()
except:
    print("Error: file not found")
    exit(0)

try:
    print('Waiting For Connection..')
    print('Connection Established From:')

    #AF_INET is IPV4 ; SOCK_STREAM is TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Waiting For Connection..')
        s.connect((HOST, PORT))
        print('Connection Established.')
        s.sendall(msg)
        print("sent:\t",msg, sep='')
        print('Waiting For reply..')
        data = s.recv(1024)
        s.close()

    print("Received:\t", data.decode(FORMAT), sep='')

    #cut 128 bytes \ 5 lines
    """
    response = data[:128]
    lines = [line for line in response.decode().splitlines()]
    for i in range(5):
        print(f"line {(i+1)}:\t", lines[i])
    """

except e:
    print("Error: connection difficulty")
    print(e)
    exit(0)

