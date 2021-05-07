import socket
from gameLogic import gameServer
from _thread import *
import sys

#Creating the array of games
games = {}

#Info about the server
server = "localhost"
port = 14201

#Other info
playersId = 0

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
    try:
        del games[gameId]
        print(f"Closed game {gameId}")
    except:
        pass
    conn.close()

while True:
    conn, addr = s.accept()
    playersId += 1
    gameId = (playersId - 1)//2

    if playersId % 2 == 1:
        games[gameId] = gameServer(playersId, None, gameId)
        print(f"Creating a new game. (Game id: {gameId} | Player 1: {playersId})")
    else:
        games[gameId].addPlayer2(playersId)
        print(f"Adding player {playersId} to game {gameId}")
        games[gameId].start()

    #Start a new thread that will be used to communicate with the player
    start_new_thread(threaded_client, (conn, playersId, 0))