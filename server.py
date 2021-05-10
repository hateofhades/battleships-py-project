#Most of the networking was done thanks to https://www.techwithtim.net/tutorials/python-online-game-tutorial/server/
import socket
from gameLogic import GameServer
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
players_id = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#Listening to the port
s.listen(2)
print("Waiting for a new connection.")

#Function thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def send_message(sock, message):
    # Prefix each message with a 4-byte length (network byte order)
    message = struct.pack('>I', len(message)) + message
    sock.sendall(message)

def threaded_client(conn, player_id, game_id):
    send_message(conn, str.encode(str(player_id)))
    reply = ""
    ok = 0

    current_game = games[game_id]

    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                print("Disconnected")
                break
            else:
                data = data.split(" ")
                if data[0] == "hit":
                    send_message(conn, pickle.dumps(current_game))
                    if player_id % 2 == 1:
                        current_game.guess_player_1(int(data[1]), int(data[2]))
                    else:
                        current_game.guess_player_2(int(data[1]), int(data[2]))
                        
                elif data[0] == "get":
                    send_message(conn, pickle.dumps(current_game))
                elif data[0] == "start":
                    send_message(conn, pickle.dumps(current_game))
                    current_game.start()
                elif data[0] == "place":
                    send_message(conn, pickle.dumps(current_game))
                    boat_type = int(data[1])
                    boat_start_x = int(data[2])
                    boat_start_y = int(data[3])
                    boat_orientation = data[4]
                    
                    player_1_or_2 = int(player_id) % 2
                    if player_1_or_2 == 0:
                        player_1_or_2 = 2

                    current_game.place_boat(boat_type, boat_start_x, boat_start_y, boat_orientation, player_1_or_2)
                elif data[0] == "reset":
                    send_message(conn, pickle.dumps(current_game))
                    current_game.reset_game()

        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print(f"Closed game {game_id}")
    except:
        pass
    conn.close()

while True:
    conn, addr = s.accept()
    players_id += 1
    game_id = (players_id - 1)//2

    if players_id % 2 == 1:
        games[game_id] = GameServer(players_id, None, game_id)
        print(f"Creating a new game. (Game id: {game_id} | Player 1: {players_id})")
    else:
        games[game_id].add_player_2(players_id)
        print(f"Adding player {players_id} to game {game_id}")
        games[game_id].start()

    #Start a new thread that will be used to communicate with the player
    start_new_thread(threaded_client, (conn, players_id, game_id))