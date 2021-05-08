import pygame
from networkClass import Network
from gameLogic import gameServer
import sys
import os


currentFolder = os.path.dirname(os.path.abspath(__file__))
backgroundImage = os.path.join(currentFolder, 'homepage_background.jpg')

pygame.init()
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

#Create Background
back_ground = pygame.image.load(backgroundImage)
bg = pygame.transform.scale(back_ground, (WIDTH, HEIGHT))

#class of in-game items
class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.n = Network()
        self.started = 0
        self.boatType = 0
        self.totalPutBoat = 0

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

                pygame.draw.line(self.window, (255, 0 ,255), (600,0), (600,600), 3)
                
                player_text1 = smallfont_ID.render("You" , True , WHITE)
                self.window.blit(player_text1,(200,550))
                player_text2 = smallfont_ID.render("Enemy" , True , WHITE)
                self.window.blit(player_text2,(800,550))
                
                #pygame.display.update()

                #init the boats
                player1Or2 = int(self.n.id) % 2
                if player1Or2 == 0:
                    player1Or2 = 2
                
                if not ((player1Or2 == 1 and game.player1EndedPlacing == 1) or (player1Or2 == 2 and game.player2EndedPlacing == 1)):
                    import random

                    cardinals = ['N', 'S', 'E', 'W']
                    v = [2, 3, 4, 6]
                    
                    orient = cardinals[0]

                    dimension = v[self.boatType]

                    txt = "Place a {} blocks boat with orientation {}".format(dimension, orient)
                    placing = smallfont_ID.render(txt , True , WHITE)
                    self.window.blit(placing,(120,570))
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            print(mouse_pos)
                            a = mouse_pos[0] // (height + margin)
                            b = mouse_pos[1] // (height + margin)
                            print(a, b)

                            if game.placeBoat(dimension, a, b, orient, player1Or2) == 1:
                                self.totalPutBoat += 1
                                if self.totalPutBoat == 4 - self.boatType:
                                    self.totalPutBoat = 0
                                    self.boatType += 1
                                #send the info to the server
                                self.n.send(f"place {dimension} {b} {a} {orient}")
                                game = self.n.send("get")
                                #draw a black  rectangle on the previous text to make the next one visible :)
                                pygame.draw.rect(self.window, BLACK, [110, 560, 700, 600])
                        pygame.display.update()  

                #Guess (self.n.send("hit x y"))
                #self.n.send("get")
                if self.started == 2:
                    if game.whoPlays == player1Or2:
                        pass
                        #Send guess to server
                pygame.display.update()            

            #Game is finished
            if self.started == 3:
                pass

            
            
            
            
            
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
