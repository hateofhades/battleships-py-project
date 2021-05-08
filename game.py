import pygame
from networkClass import Network
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
# 
#Create Background
back_ground = pygame.image.load(backgroundImage)
bg = pygame.transform.scale(back_ground, (WIDTH, HEIGHT))

#class of in-game items
class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.n = Network()
        print(self.n.send("Hello bois"))

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
            for event in pygame.event.get():
            # check if the player has closed the game   
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                
                #ID box responsive to the mouse of the player
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
                            self.window.fill(BLACK)
                            clicked = True

                            #draw the tables
                            height = 47
                            margin = 5
                            for row in range(10):
                                for column in range(10):
                                    color = BLUE
                                    """ if grid1[row][column] == 1:
                                        color = RED
                                    if grid1[row][column] == 2:
                                        color = BLACK """
                                    pygame.draw.rect(self.window, (0, 192, 192), [(margin + height) * column + margin, (margin + height) * row + margin, height, height])
                            
                            for row in range(10):
                                for column in range(10):
                                    color = BLUE
                                    """ if grid2[row][column] == 1:
                                        color = RED
                                    if grid2[row][column] == 2:
                                        color = BLACK """
                                    pygame.draw.rect(self.window, BLUE, [660 + (margin + height) * column + margin, (margin + height) * row + margin, height, height])

                            pygame.draw.line(self.window, (255, 0 ,255), (600,0), (600,600), 3)
                            
                            player_text1 = smallfont_ID.render('Player 1: ' , True , WHITE)
                            self.window.blit(player_text1,(200,550))
                            player_text2 = smallfont_ID.render('Player 2: ' , True , WHITE)
                            self.window.blit(player_text2,(800,550))
                            
                            pygame.display.update()
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
