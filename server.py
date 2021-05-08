#Most of the networking was done thanks to https://www.techwithtim.net/tutorials/python-online-game-tutorial/server/
import socket
from gameLogic import gameServer
from _thread import *
import sys
import pickle
import struct

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

#Function thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def threaded_client(conn, playerId, gameId):
    send_msg(conn, str.encode(str(playerId)))
    reply = ""
    ok = 0

    currentGame = games[gameId]

    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                print("Disconnected")
                break
            else:
                data = data.split(" ")
                if data[0] == "hit":
                    send_msg(conn, pickle.dumps(currentGame))
                    print(data[1],data[2])
                    if playerId % 2 == 1:
                        print(currentGame.guessPlayer1(int(data[1]), int(data[2])))
                    else:
                        currentGame.guessPlayer2(int(data[1]), int(data[2]))
                        
                elif data[0] == "get":
                    send_msg(conn, pickle.dumps(currentGame))
                elif data[0] == "start":
                    send_msg(conn, pickle.dumps(currentGame))
                    currentGame.start()
                elif data[0] == "place":
                    send_msg(conn, pickle.dumps(currentGame))
                    boatType = int(data[1])
                    boatStartX = int(data[2])
                    boatStartY = int(data[3])
                    boatOrientation = data[4]
                    
                    player1Or2 = int(playerId) % 2
                    if player1Or2 == 0:
                        player1Or2 = 2

                    currentGame.placeBoat(boatType, boatStartX, boatStartY, boatOrientation, player1Or2)
                elif data[0] == "reset":
                    send_msg(conn, pickle.dumps(currentGame))
                    currentGame.resetGame()

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
    start_new_thread(threaded_client, (conn, playersId, gameId))