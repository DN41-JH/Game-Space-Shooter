import pygame
import os
import time
import random
pygame.font.init()

# Below set up the gaming window
width = 750
height = 900
WINDOW = pygame.display.set_mode((width, height)) # This specifies the width and height of the game window
pygame.display.set_caption("Space Invader") # This specifies the caption of the game window

# Below load the ship images
red_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
blue_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
green_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
player_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Below load the bullet images
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Below load the background image
background_black = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (width, height))



class Ship:
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_image = None
		self.laser_image = None
		self.lasers = []
		self.cool_down_counter = 0

	def draw(self, window):
		pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50), 2)




def main():
	run = True # Decides whether the proceed the game
	FPS = 60 # Frame-Per-Second, the rate of the game to be running
	level = 1 # Indicates the current game level
	lives = 5 # Indicates the number of lives remaining
	ship_velocity = 5

	game_font = pygame.font.SysFont("comicsans", 50) # This specifies the font and size of the text label in the game


	ship = Ship(300, 650)



	clock = pygame.time.Clock()

	def update_window():
		WINDOW.blit(background_black, (0,0)) # Took the background_black image, and draw it at coordinate (0,0) on the game WINDOW
		
		# Below update and draw the text labels on the game window:
		level_label = game_font.render("Level: " + str(level), 1, (255,0,0)) # Update the text level label on the game window
		lives_label = game_font.render("Lives: " + str(lives), 1, (0,255,0)) # Update the text lives label on the game window
		WINDOW.blit(level_label, (10,10))
		WINDOW.blit(lives_label, (width - level_label.get_width() - 10, 10))


		ship.draw(WINDOW)


		pygame.display.update()


	while run:
		clock.tick(FPS) # Tick the clock with the rate specified by "FPS"
		update_window()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:  ### This is the way to stop and quit the game
				run = False

		key = pygame.key.get_pressed()
		if key[pygame.K_a] or key[pygame.K_LEFT]: # "a" or "left" being pressed, move the ship left
			ship.x = ship.x - ship_velocity
		if key[pygame.K_d] or key[pygame.K_RIGHT]: # "d" or "right" being pressed, move the ship right
			ship.x = ship.x + ship_velocity
		if key[pygame.K_w] or key[pygame.K_UP]: # "w" or "up" being pressed, move the ship up
			ship.y = ship.y - ship_velocity
		if key[pygame.K_s] or key[pygame.K_DOWN]: # "s" or "down" being pressed, move the ship down
			ship.y = ship.y + ship_velocity





main()