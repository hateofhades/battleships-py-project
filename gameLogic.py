import numpy as np

class gameServer:
    def __init__(self, playerId1, playerId2, gameId):
        self.player1 = playerId1
        self.player2 = playerId2
        self.gameId = gameId
        self.started = 0
        self.whoPlays = 1

    #Will return 0 if game ended or didn't start
    def isPlaying(self):
        return self.started
    
    #Returns the status of the game (whose turn, table state, guesses made)
    def getGameState(self):
        return (self.isPlaying, self.whoPlays, self.player1Table, self.player2Table, self.player1Guessed, self.player2Guessed)

    #Return who plays
    def whichPlayerTurn(self):
        return self.whoPlays

    def addPlayer1(self, playerId1):
        self.player1 = playerId1
    
    def addPlayer2(self, playerId2):
        self.player2 = playerId2

    #Starting the game
    def start(self):
        if self.player1 == None or self.player2 == None:
            return "Can't start game with 1 player"
        
        #Create the tables and put status to started
        self.started = 1
        self.player1Table = np.zeros((10, 10))
        self.player2Table = np.zeros((10, 10))
        self.player1Guessed = np.zeros((10, 10))
        self.player2Guessed = np.zeros((10, 10))
    
    def guessPlayer1(self, x, y):
        #If it's not player 1 turn return with error code -1
        if self.whoPlays == 2: 
            return -1

        #If already guessed return with error code -2
        if self.player1Guessed[x][y] != 0:
            return -2
        
        #Get if there was a ship on player2's table, and update guessed accordingly and return it
        #If missed the other player plays next
        if self.player2Table[x][y] != 0:
            self.player1Guessed[x][y] = 2
        else:
            self.player1Guessed[x][y] = 1
            self.whoPlays = 2
        
        return self.player1Guessed[x][y]
    
    def guessPlayer2(self, x, y):
        #If it's not player 2 turn return with error code -1
        if self.whoPlays == 1: 
            return -1

        #If already guessed return with error code -2
        if self.player2Guessed[x][y] != 0:
            return -2
        
        #Get if there was a ship on player1's table, and update guessed accordingly and return it
        #If missed the other player plays next
        if self.player1Table[x][y] != 0:
            self.player2Guessed[x][y] = 2
        else:
            self.player2Guessed[x][y] = 1
            self.whoPlays = 1

        return self.player2Guessed[x][y]