import pygame
import sys

pygame.init()
frame_rate = pygame.time.Clock()

#globals
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

dark_color_for_play_button = (1,50,32)
light_color_for_play_button = (135,190,144)

WIDTH = 1200
HEIGHT = 900
#create font for the play button
smallfont = pygame.font.SysFont('Corbel',200)
text = smallfont.render('PLAY' , True , WHITE)

#!!!To work, the path to the image must be changed
back_ground = pygame.image.load('/Users/iulia-andreea_grigore/Desktop/py/py_proj/homepage_background.jpg')
bg = pygame.transform.scale(back_ground, (WIDTH, HEIGHT))

#class of in-game items
class Game:
	
	def __init__(self):
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Battleships")

	def draw(self):
		
		running = True
		while running:
			for event in pygame.event.get():
			# check if the player has closed the game   
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
			#check if the player has started the game and change the background if so
				if event.type == pygame.MOUSEBUTTONDOWN:
					if 350 <= mouse[0] <= 850 and 350 <= mouse[1] <= 500:
						pygame.quit()

			#background of the home page
			self.window.blit(bg, (0,0))

			#check the position of the player's mouse 
			# and change the color of the play button, depending on it
			mouse = pygame.mouse.get_pos()
			if 350 <= mouse[0] <= 850 and 350 <= mouse[1] <= 500:
				pygame.draw.rect(self.window,light_color_for_play_button,[350, 350, 500, 150])
			else:
				pygame.draw.rect(self.window, dark_color_for_play_button,[350, 350, 500, 150])

			#the position of the Play botton text
			self.window.blit(text ,(418,365))

			pygame.display.update()
		
