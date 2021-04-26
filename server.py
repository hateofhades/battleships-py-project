import socket
from _thread import *
import sys

#Info about the server
server = "localhost"
port = 14201

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#Listening to the port
s.listen(2)
print("Waiting for a new connection.")

def threaded_client(conn, playerId, gameId):
    conn.send(str.encode(str(playerId)))
    reply = ""
    ok = 0

    while True:
        try:
            data = conn.recv(2048).decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                if data == "1":
                    ok += 1

            conn.sendall(str.encode(str(ok)))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}. Assigned playerId: {1}.")

    #Start a new thread that will be used to communicate with the player
    start_new_thread(threaded_client, (conn, 1, 0))