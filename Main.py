import pygame
import os
import time
import random
pygame.font.init()

# Below set up the gaming window
width = 750
height = 900
WINDOW = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")

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

def main():
	run = True # Decides whether the proceed the game
	FPS = 60 # Frame-Per-Second, the rate of the game to be running
	level = 1
	lives = 5
	game_font = pygame.font.SysFont("comicsans", 50)

	clock = pygame.time.Clock()

	def update_window():
		WINDOW.blit(background_black, (0,0)) # Took the background_black image, and draw it at coordinate (0,0) on the game WINDOW
		
		# Below draw the text on the game window:
		level_label = game_font.render("Level: " + str(level), 1, (255,0,0))
		lives_label = game_font.render("Lives: " + str(lives), 1, (0,255,0))


		WINDOW.blit(lives_label, (10,10))
		WINDOW.blit(level_label, (width - level_label.get_width() - 10, 10))


		pygame.display.update()


	while run:
		clock.tick(FPS) # Tick the clock with the rate specified by "FPS"
		update_window()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:  ### This is the way to stop and quit the game
				run = False

main()