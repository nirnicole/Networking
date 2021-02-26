#!/usr/bin/env python3
import sqlite3
from contextlib import closing

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)
MAX_LINES = 5
MAX_BYTES = 128
FORMAT = "utf-8"
lines = []

# use a txt file
"""
try:
    f = open("message.txt")
    msg = f.read().encode()
    f.close()
except:
    print("Error: file not found")
    exit(0)
"""

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)      #recive only 1024 bytes
                if not data:
                    break
                print(data.decode(FORMAT)) #display input

                # cut 128 bytes \ 5 lines
                response = data[:MAX_BYTES].decode(FORMAT)
                lines = response.splitlines()
                edited_response = ''
                for i in range( min(len(lines), MAX_LINES) ):
                    edited_response+=(lines[i]+'\n')

                data = edited_response.encode(FORMAT)

                #just echo back
                conn.sendall(data)
except e:
    print("Error: connection difficulty")
    print(e)
    exit(0)


# create and fill an sql table
with closing(sqlite3.connect("messages.db")) as connection:
    with closing(connection.cursor()) as cursor:
        try:
            cursor.execute("CREATE TABLE messages (message_id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)")
        except sqlite3.OperationalError:
            print("Error, messages.db already exist")

        for i in range(min(len(lines), MAX_LINES)):
            cursor.execute("INSERT INTO messages VALUES (null,?)", (lines[i],))

        rows = cursor.execute("SELECT * FROM messages").fetchall()
        print(rows)