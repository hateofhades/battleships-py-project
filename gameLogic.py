import numpy as np

class gameServer:
    def __init__(self, playerId1, playerId2, gameId):
        self.player1 = playerId1
        self.player2 = playerId2
        self.gameId = gameId
        self.started = 0
        self.whoPlays = 1
        self.won = 0

        self.player1Table = np.zeros((10, 10))
        self.player2Table = np.zeros((10, 10))
        self.player1Guessed = np.zeros((10, 10))
        self.player2Guessed = np.zeros((10, 10))       

        self.player1Boats = 0
        self.player2Boats = 0

        self.player1EndedPlacing = 0
        self.player2EndedPlacing = 0

    #Very bad code needs a lot of refractoring
    #First checks if initial and last positions are valid (if not returns error code -1)
    #Then checks if all positions are unnocupied (if not returns error code -2)
    #If all are unnocupied occupy them
    def placeBoat(self, boatType, boatStartX, boatStartY, boatOrientation, playerId):
        if self.isPlaying == 1:
            return -3
        if boatStartX < 0 or boatStartX >= 10 or boatStartY < 0 or boatStartY >= 10:
            return -1
        if playerId == 1:
            if boatOrientation == "S":
                if(boatStartX + boatType - 1 < 0 or boatStartX + boatType - 1 >= 10):
                    return -1

                validPlacement = 1

                for x in range(boatStartX, boatStartX + boatType):
                    if self.player1Table[x][boatStartY] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for x in range(boatStartX, boatStartX + boatType):
                        self.player1Table[x][boatStartY] = 1
                    
                    self.player1Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "E":
                if(boatStartY + boatType - 1 < 0 or boatStartY + boatType - 1 >= 10):
                    return -1

                validPlacement = 1

                for y in range(boatStartY, boatStartY + boatType):
                    if self.player1Table[boatStartX][y] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for y in range(boatStartY, boatStartY + boatType):
                        self.player1Table[boatStartX][y] = 1
                    
                    self.player1Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "N":
                if(boatStartX - boatType + 1 < 0 or boatStartX - boatType + 1 >= 10):
                    return -1

                validPlacement = 1

                for x in range(boatStartX - boatType + 1, boatStartX + 1):
                    if self.player1Table[x][boatStartY] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for x in range(boatStartX - boatType + 1, boatStartX + 1):
                        self.player1Table[x][boatStartY] = 1
                    
                    self.player1Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "W":
                if(boatStartY - boatType + 1 < 0 or boatStartY - boatType + 1 >= 10):
                    return -1

                validPlacement = 1

                for y in range(boatStartY - boatType + 1, boatStartY + 1):
                    if self.player1Table[boatStartX][y] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for y in range(boatStartY - boatType + 1, boatStartY + 1):
                        self.player1Table[boatStartX][y] = 1
                    
                    self.player1Boats += boatType
                    return 1
                else:
                    return -2
        elif playerId == 2:
            if boatOrientation == "S":
                if(boatStartX + boatType - 1 < 0 or boatStartX + boatType - 1 >= 10):
                    return -1

                validPlacement = 1

                for x in range(boatStartX, boatStartX + boatType):
                    if self.player2Table[x][boatStartY] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for x in range(boatStartX, boatStartX + boatType):
                        self.player2Table[x][boatStartY] = 1
                    
                    self.player2Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "E":
                if(boatStartY + boatType - 1 < 0 or boatStartY + boatType - 1 >= 10):
                    return -1

                validPlacement = 1

                for y in range(boatStartY, boatStartY + boatType):
                    if self.player2Table[boatStartX][y] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for y in range(boatStartY, boatStartY + boatType):
                        self.player2Table[boatStartX][y] = 1
                    
                    self.player2Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "N":
                if(boatStartX - boatType + 1 < 0 or boatStartX - boatType + 1 >= 10):
                    return -1

                validPlacement = 1

                for x in range(boatStartX - boatType + 1, boatStartX + 1):
                    if self.player2Table[x][boatStartY] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for x in range(boatStartX - boatType + 1, boatStartX + 1):
                        self.player2Table[x][boatStartY] = 1
                    
                    self.player2Boats += boatType
                    return 1
                else:
                    return -2
            elif boatOrientation == "W":
                if(boatStartY - boatType + 1 < 0 or boatStartY - boatType + 1 >= 10):
                    return -1

                validPlacement = 1

                for y in range(boatStartY - boatType + 1, boatStartY + 1):
                    if self.player2Table[boatStartX][y] != 0:
                        validPlacement = 0
                        break
                
                if validPlacement == 1:
                    for y in range(boatStartY - boatType + 1, boatStartY + 1):
                        self.player2Table[boatStartX][y] = 1
                    
                    self.player2Boats += boatType
                    return 1
                else:
                    return -2
        
        if self.player1Boats == self.player2Boats and self.player2Boats == 31:
            self.isPlaying = 2

    #Will return 0 if game ended or didn't start
    def isPlaying(self):
        return self.started
    
    def play(self, data):
        pass

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

        self.started = 1
    
    def guessPlayer1(self, x, y):
        if self.isPlaying != 2:
            return -1
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
            self.player2Boats -= 1

            if self.player2Boats == 0:
                self.isPlaying = 3
                self.won = "1"
        else:
            self.player1Guessed[x][y] = 1
            self.whoPlays = 2
        
        return self.player1Guessed[x][y]
    
    def guessPlayer2(self, x, y):
        if self.isPlaying != 2:
            return -1
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
            self.player1Boats -= 1

            if self.player1Boats == 0:
                self.isPlaying = 3
                self.won = "2"
        else:
            self.player2Guessed[x][y] = 1
            self.whoPlays = 1

        return self.player2Guessed[x][y]