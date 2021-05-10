import pygame
from networkClass import Network
from gameLogic import gameServer
import sys
import os                    
import random

currentFolder = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.mixer.init()

hit = pygame.mixer.Sound(os.path.join(currentFolder, 'hit.wav'))
miss = pygame.mixer.Sound(os.path.join(currentFolder, 'miss.wav'))
yourturn = pygame.mixer.Sound(os.path.join(currentFolder, 'yourTurn.wav'))
win = pygame.mixer.Sound(os.path.join(currentFolder, 'win.wav'))
lose = pygame.mixer.Sound(os.path.join(currentFolder, 'lose.wav'))


frame_rate = pygame.time.Clock()

#globals
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0 ,0)
BOATCOLOR = (255, 255, 255)


dark_color_for_play_button = (1,50,32)
light_color_for_play_button = (135,190,144)

WIDTH = 1200
HEIGHT = 600

#create font for the play button
smallfont = pygame.font.SysFont('Corbel',200)
text = smallfont.render('PLAY' , True , WHITE)

#create font for ID boxes and add colors for them
base_font = pygame.font.Font(None, 32)
rectangle_box_active_color = (114,121,121)
rectangle_box_passive_color = WHITE
smallfont_ID = pygame.font.SysFont('Corbel',32)
id_text = smallfont_ID.render('Player ID: ' , True , WHITE)


#class of in-game items
class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.n = Network()
        print(self.n.id)
        self.started = 0
        self.boatType = 0
        self.totalPutBoat = 0
        self.orientation_number = 0
        self.starting = 0
        self.last = 0
        self.winLoseSound = 0

    def draw(self):
        self.user_id = self.n.id
        running = True

        #using cliked variable to see if the play button was clicked
        clicked = False

        #rectangle box to enter the player ID
        rectangle_box = pygame.Rect(620,520,160,35)
        color = rectangle_box_passive_color
        active = False

        while running:
            game = gameServer(None, None, None)
            game = self.n.send("get")
            self.started = game.isPlaying()

            if self.started == 1 or self.started == 2:
                self.window.fill(BLACK)
                clicked = True

                pygame.draw.line(self.window, (0, 250, 154), (600,0), (600,600), 3)
                
                player_text1 = smallfont_ID.render("You" , True , WHITE)
                self.window.blit(player_text1,(250,540))
                player_text2 = smallfont_ID.render("Enemy" , True , WHITE)
                self.window.blit(player_text2,(887,540))

                #draw the board
                height = 47
                margin = 5

                for row in range(10):
                        for column in range(10):
                            pygame.draw.rect(self.window, BLUE, [(margin + height) * column + margin, (margin + height) * row + margin, height, height])
                            pygame.draw.rect(self.window, BLUE, [660 + (margin + height) * column + margin, (margin + height) * row + margin, height, height])

                if int(self.n.id) % 2 == 1: 
                    for row in range(10):
                        for column in range(10):
                            if game.player1Table[row][column] == 1:
                                pygame.draw.rect(self.window, BOATCOLOR, [(margin + height) * column + margin, (margin + height) * row + margin, height, height])  
                            if game.player2Guessed[row][column] == 1:
                                pygame.draw.rect(self.window, BLACK, [(margin + height) * column + margin, (margin + height) * row + margin, height, height])
                            if game.player2Guessed[row][column] == 2:
                                pygame.draw.rect(self.window, RED, [(margin + height) * column + margin, (margin + height) * row + margin, height, height])
                        
                    for row in range(10):
                        for column in range(10):
                            color = BLUE
                            if game.player1Guessed[row][column] == 1:
                                color = BLACK
                            if game.player1Guessed[row][column] == 2:
                                color = RED
                            pygame.draw.rect(self.window, color, [660 + (margin + height) * column + margin, (margin + height) * row + margin, height, height])

                else:
                    for row in range(10):
                        for column in range(10):
                            color = BLUE
                            if game.player2Guessed[row][column] == 1:
                                color = BLACK
                            if game.player2Guessed[row][column] == 2:
                                color = RED
                            pygame.draw.rect(self.window, color, [660 + (margin + height) * column + margin, (margin + height) * row + margin, height, height])
                        
                    for row in range(10):
                        for column in range(10):
                            if game.player2Table[row][column] == 1:
                                pygame.draw.rect(self.window, BOATCOLOR, [(margin + height) * column + margin, (margin + height) * row + margin, height, height])  
                            if game.player1Guessed[row][column] == 1:
                                pygame.draw.rect(self.window, BLACK, [(margin + height) * column + margin, (margin + height) * row + margin, height, height]) 
                            if game.player1Guessed[row][column] == 2:
                                pygame.draw.rect(self.window, RED, [(margin + height) * column + margin, (margin + height) * row + margin, height, height]) 
                

                #init the boats
                player1Or2 = int(self.n.id) % 2
                if player1Or2 == 0:
                    player1Or2 = 2
                
                if game.isPlaying() == 1:
                    if self.starting == 0:
                        self.starting = 1
                        yourturn.play()

                    cardinals = ['N', 'S', 'E', 'W']
                    v = [2, 3, 4, 6]
                    
                    orient = cardinals[self.orientation_number]

                    if self.boatType < 4:
                        dimension = v[self.boatType]
                    else:
                        dimension = 0

                    if dimension > 0:
                        txt = "Place a {} blocks boat with orientation {}".format(dimension, orient)
                        placing = smallfont_ID.render(txt , True , WHITE)
                        self.window.blit(placing,(120,570))
                        
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                
                                a = mouse_pos[0] // (height + margin)
                                b = mouse_pos[1] // (height + margin)

                                if game.placeBoat(dimension, a, b, orient, player1Or2) == 1:
                                    self.totalPutBoat += 1
                                    if self.totalPutBoat == 4 - self.boatType:
                                        self.totalPutBoat = 0
                                        self.boatType += 1

                                    #send the info to the server
                                    self.n.send(f"place {dimension} {a} {b} {orient}")
                                    game = self.n.send("get")
                                    
                                    #draw a black  rectangle on the previous text to make the next one visible :)
                                    pygame.draw.rect(self.window, BLACK, [110, 540, 700, 600])
                            if event.type == pygame.KEYDOWN:
                                if event.key == 114:
                                    self.orientation_number +=1
                                    if self. orientation_number == 4:
                                        self.orientation_number = 0 
                    else:
                        if game.isPlaying() == 2:
                            pygame.draw.rect(self.window, BLACK, [110, 540, 700, 600])
                        else:
                            placing = smallfont_ID.render("Wait for opponent to place their boats" , True , WHITE)
                            self.window.blit(placing,(120,560))
                    
                    pygame.display.update()  

                #Guess 
                if self.started == 2:
                    if self.last != game.whoPlays:
                        self.starting = 0
                        self.last = game.whoPlays

                    if game.whoPlays == player1Or2:
                        if self.starting == 0:
                            yourturn.play()
                            self.starting = 1

                        placing = smallfont_ID.render("Time to guess!" , True , WHITE)
                        self.window.blit(placing,(120,560))
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                print(mouse_pos)
                                
                                a = (mouse_pos[0] - 660) // (height + margin)
                                b = mouse_pos[1] // (height + margin)
                                print(a,b)
                                if a >= 0 and b >= 0:
                                    pygame.mixer.stop()
                                    self.n.send(f"hit {b} {a}")
                                    if (player1Or2 == 1 and game.guessPlayer1(b, a) == 1) or (player1Or2 == 2 and game.guessPlayer2(b, a) == 1):
                                        miss.play()
                                    else:
                                        hit.play()
                                game = self.n.send("get")
                        
                    else:
                        placing = smallfont_ID.render("Waiting for opponent!" , True , WHITE)
                        self.window.blit(placing,(120,560))
                        #Send guess to server
                pygame.display.update()  

            #Game is finished
            elif self.started == 3:
                if self.winLoseSound == 0:
                    pygame.mixer.stop()
                    if game.won == player1Or2:
                        win.play()
                    else:
                        lose.play()

                    self.winLoseSound = 1

                #Draw the final background image
                backgroundImage = os.path.join(currentFolder, 'final_background.jpeg')
                back_ground = pygame.image.load(backgroundImage)
                bg = pygame.transform.scale(back_ground, (WIDTH, HEIGHT))
                self.window.blit(bg, (0,0))

                #Draw the bow that show the winner
                smallfont_winner_box = pygame.font.SysFont('Corbel',60)
                player_text1 = smallfont_winner_box.render(f"The winner is: {game.won}" , True , WHITE)
                self.window.blit(player_text1,(445,550))
            
            for event in pygame.event.get():
            # check if the player has closed the game   
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                
                #ID box responsive to the mouse of the player
                if self.started == 0:
                    if clicked == False:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if rectangle_box.collidepoint(event.pos):
                                active = True
                            else:
                                active = False
                        if event.type == pygame.KEYDOWN:
                            if active == True:
                                if event.key == pygame.K_BACKSPACE:
                                    self.user_id = self.user_id[:-1]
                                else:
                                    self.user_id += event.unicode

                        #background of the home page
                        backgroundImage = os.path.join(currentFolder, 'homepage_background.jpg')
                        back_ground = pygame.image.load(backgroundImage)
                        bg = pygame.transform.scale(back_ground, (WIDTH, HEIGHT))
                        self.window.blit(bg, (0,0))

                        #active functionality of the mouse box ID
                        if active:
                            color = rectangle_box_active_color
                        else:
                            color = rectangle_box_passive_color

                        #check the position of the player's mouse 
                        # and change the color of the play button, depending on it
                        mouse = pygame.mouse.get_pos()
                        if 350 <= mouse[0] <= 850 and 350 <= mouse[1] <= 500:
                            pygame.draw.rect(self.window,light_color_for_play_button,[350, 350, 500, 150])

                            #check if the player has started the game and change the background if so
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                #Check if game can be started!!! (Send a request to the server to start the game and then send a request
                                # to get newest gamestate, so we can check if the game has started)
                                self.n.send("start")
                                game = self.n.send("get")
                        else:
                            pygame.draw.rect(self.window, dark_color_for_play_button,[350, 350, 500, 150])

                        #draw the ID boxes
                        if clicked == False:
                            pygame.draw.rect(self.window,rectangle_box_active_color, [430, 520, 160, 35], 2)
                            pygame.draw.rect(self.window, rectangle_box_active_color, rectangle_box)
                            text_surface = base_font.render(self.user_id, True, WHITE)
                            self.window.blit(text_surface, (rectangle_box.x + 5, rectangle_box.y + 5))
                            rectangle_box.w = max(150, text_surface.get_width() + 10)
                            
                    
                    
                    if clicked == False:
                        #draw the texts from the buttons
                        self.window.blit(text ,(418,365))
                        self.window.blit(id_text, (462,528))

                pygame.display.update()
