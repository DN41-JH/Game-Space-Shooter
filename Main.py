import pygame
import os
import time
import random
pygame.font.init(*)

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
	clock = pygame.time.Clock()

	def update_window():
		WINDOW.blit(background_black, (0,0)) # Took the background_black image, and draw it at coordinate (0,0) on the game WINDOW
		pygame.display.update()


	while run:
		clock.tick(FPS) # Tick the clock with the rate specified by "FPS"
		update_window()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:  ### This is the way to stop and quit the game
				run = False