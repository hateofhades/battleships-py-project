import numpy as np

class GameServer:
    def __init__(self, player_id_1, player_id_2, game_id):
        
        self.player_1 = player_id_1
        self.player_2 = player_id_2

        self.game_id = game_id
        self.started = 0
        self.who_plays = 1
        self.won = 0

        self.player_1_table = np.zeros((10, 10))
        self.player_2_table = np.zeros((10, 10))

        self.player_1_guessed = np.zeros((10, 10))
        self.player_2_guessed = np.zeros((10, 10))       

        self.player_1_boats = 0
        self.player_2_boats = 0

        self.player_1_ended_placing = 0
        self.player_1_ended_placing = 0
        
    #First checks if initial and last positions are valid (if not returns error code -1)
    #Then checks if all positions are unnocupied (if not returns error code -2)
    #Returns 0 if game is not in place mode
    #If all are unnocupied occupy them and return 1
    def place_boat(self, boat_type, boat_start_x, boat_start_y, boat_orientation, player_id):
        if self.is_playing() != 1:
            return 0
        if boat_start_x >= 10 or boat_start_x < 0 or boat_start_y >= 10 or boat_start_y < 0:
            return -1
        
        valid_player_1 = 1
        valid_player_2 = 1

        if boat_orientation == "N":
            boat_end_y = boat_start_y - boat_type + 1
            if boat_end_y >= 10 or boat_end_y < 0:
                return -1

            for y in range(boat_end_y, boat_start_y + 1):
                if self.player_1_table[y][boat_start_x] != 0:
                    valid_player_1 = 0
                if self.player_2_table[y][boat_start_x] != 0:
                    valid_player_2 = 0
            
            if player_id == 1 and valid_player_1 == 1:
                self.player_1_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for y in range(boat_end_y, boat_start_y + 1):
                    self.player_1_table[y][boat_start_x] = 1
                return 1

            elif player_id == 2 and valid_player_2 == 1:
                self.player_2_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for y in range(boat_end_y, boat_start_y + 1):
                    self.player_2_table[y][boat_start_x] = 1
                return 1
            return -1

        elif boat_orientation == "S":
            boat_end_y = boat_start_y + boat_type - 1
            if boat_end_y >= 10 or boat_end_y < 0:
                return -1
            
            for y in range(boat_start_y, boat_end_y + 1):
                if self.player_1_table[y][boat_start_x] != 0:
                    valid_player_1 = 0
                if self.player_2_table[y][boat_start_x] != 0:
                    valid_player_2 = 0
            
            if player_id == 1 and valid_player_1 == 1:
                self.player_1_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for y in range(boat_start_y, boat_end_y + 1):
                    self.player_1_table[y][boat_start_x] = 1
                return 1

            elif player_id == 2 and valid_player_2 == 1:
                self.player_2_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for y in range(boat_start_y, boat_end_y + 1):
                    self.player_2_table[y][boat_start_x] = 1
                return 1
            return -1

        elif boat_orientation == "E":
            boat_end_x = boat_start_x + boat_type - 1
            if boat_end_x >= 10 or boat_end_x < 0:
                return -1
            
            for x in range(boat_start_x, boat_end_x + 1):
                if self.player_1_table[boat_start_y][x] != 0:
                    valid_player_1 = 0
                if self.player_2_table[boat_start_y][x] != 0:
                    valid_player_2 = 0
            
            if player_id == 1 and valid_player_1 == 1:
                self.player_1_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for x in range(boat_start_x, boat_end_x + 1):
                    self.player_1_table[boat_start_y][x] = 1
                return 1

            elif player_id == 2 and valid_player_2 == 1:
                self.player_2_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for x in range(boat_start_x, boat_end_x + 1):
                    self.player_2_table[boat_start_y][x] = 1
                return 1
            return -1

        elif boat_orientation == "W":
            boat_end_x = boat_start_x - boat_type + 1
            if boat_end_x >= 10 or boat_end_x < 0:
                return -1

            for x in range(boat_end_x, boat_start_x + 1):
                if self.player_1_table[boat_start_y][x] != 0:
                    valid_player_1 = 0
                if self.player_2_table[boat_start_y][x] != 0:
                    valid_player_2 = 0
            
            if player_id == 1 and valid_player_1 == 1:
                self.player_1_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for x in range(boat_end_x, boat_start_x + 1):
                    self.player_1_table[boat_start_y][x] = 1
                return 1
                
            elif player_id == 2 and valid_player_2 == 1:
                self.player_2_boats += 1
                if self.player_1_boats == 10 and self.player_2_boats == 10:
                    self.started = 2
                    self.player_1_boats = 31
                    self.player_2_boats = 31
                for x in range(boat_end_x, boat_start_x + 1):
                    self.player_2_table[boat_start_y][x] = 1
                return 1
            return -1


    #Will return 0 if game ended or didn't start
    def is_playing(self):
        return self.started
    
    def play(self, data):
        pass

    #Returns the status of the game (whose turn, table state, guesses made)
    def get_game_state(self):
        return (self.is_playing, self.who_plays, self.player_1_table, self.player_2_table, self.player_1_guessed, self.player_2_guessed)

    #Return who plays
    def which_player_turn(self):
        return self.who_plays

    def add_player_1(self, player_id_1):
        self.player_1 = player_id_1
    
    def add_player_2(self, player_id_2):
        self.player_2 = player_id_2

    #Starting the game
    def start(self):
        if self.player_1 == None or self.player_2 == None:
            return "Can't start game with 1 player"

        self.started = 1
    
    def guess_player_1(self, x, y):
        if self.is_playing() != 2:
            return -1
        #If it's not player 1 turn return with error code -1
        if self.who_plays == 2: 
            return -1

        #If already guessed return with error code -2
        if self.player_1_guessed[x][y] != 0:
            return -2
        
        #Get if there was a ship on player_2's table, and update guessed accordingly and return it
        #If missed the other player plays next
        if self.player_2_table[x][y] != 0:
            self.player_1_guessed[x][y] = 2
            self.player_2_boats -= 1

            if self.player_2_boats == 0:
                self.started = 3
                self.won = 1
        else:
            self.player_1_guessed[x][y] = 1
            self.who_plays = 2
        
        return self.player_1_guessed[x][y]
    
    def guess_player_2(self, x, y):
        if self.is_playing() != 2:
            return -1
        #If it's not player 2 turn return with error code -1
        if self.who_plays == 1: 
            return -1

        #If already guessed return with error code -2
        if self.player_2_guessed[x][y] != 0:
            return -2
        
        #Get if there was a ship on player_1's table, and update guessed accordingly and return it
        #If missed the other player plays next
        if self.player_1_table[x][y] != 0:
            self.player_2_guessed[x][y] = 2
            self.player_1_boats -= 1

            if self.player_1_boats == 0:
                self.started = 3
                self.won = 2
        else:
            self.player_2_guessed[x][y] = 1
            self.who_plays = 1

        return self.player_2_guessed[x][y]