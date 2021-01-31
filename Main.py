import pygame
import os
import time
import random
pygame.font.init()

# Below set up the gaming window
width = 950
height = 950
WINDOW = pygame.display.set_mode((width, height)) # This specifies the width and height of the game window
pygame.display.set_caption("Sky Protector") # This specifies the caption of the game window

# Below load the ship images
white_ship = pygame.image.load(os.path.join("assets", "Enemy_ship_white.png"))
yellow_ship = pygame.image.load(os.path.join("assets", "Enemy_ship_yellow.png"))
blue_ship = pygame.image.load(os.path.join("assets", "Enemy_ship_blue.png"))
player_ship = pygame.image.load(os.path.join("assets", "Player_ship1.png"))

# Below load the laser bullet images
red_laser = pygame.image.load(os.path.join("assets", "Laser_red.png"))
green_laser = pygame.image.load(os.path.join("assets", "Laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "Laser_blue.png"))
player_laser = pygame.image.load(os.path.join("assets", "Laser_player.png"))

# Below load the background image
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_universe.jpg")), (width, height)) # Re-scale the size of the background into the size of the gaming window

class Laser:
	def __init__(self, x, y, image): # Define the property of the Laser class
		self.x = x
		self.y = y
		self.image = image
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, WINDOW): # Draw method, aims to draw the laser onto the game window
		WINDOW.blit(self.image, (self.x, self.y))

	def move(self, velocity): # Move method, aims to vertically move the laser on the game window
		self.y = self.y + velocity

	def off_screen(self, height): # Off_screen method, aims to detect whether the laser is outside of the game window
		return not(self.y <= height and self.y >=0)

	def collision(self, object): # Collision method, aims to detect whether the laser bullet hits other flights
		return collide(object, self)


class Ship:
	CoolDown = 15 ### This is the bullet firing cool down time, the higher CoolDown is, the fewer bullet one is allowed shoot in an unit amount of time

	def __init__(self, x, y, health=100): # Define the property of the Ship class, where the health of the ship is set to be 100 by default
		self.x = x
		self.y = y
		self.health = health
		self.ship_image = None
		self.laser_image = None
		self.lasers = []
		self.cool_down_counter = 0

	def cool_down(self): # Cool_down method, aims to control the cool-down mechanism of firing the laser bullet: able to fire the laser if and only if when cool_down_counter goes beyond "CoolDown"
		if 0 < self.cool_down_counter < self.CoolDown:
			self.cool_down_counter = self.cool_down_counter + 1
		elif self.cool_down_counter >= self.CoolDown:
			self.cool_down_counter = 0

	def shoot(self): # Shoot method, aims to shoot the laser bullet, after conditionally checking whether cool_down_counter is satisfied
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_image)
			self.lasers.append(laser)
			self.cool_down_counter += 1 

	def move_lasers(self, velocity, object): # Move_lasers method, aims to check whether the laser (fired by the flight) is out of the window, or if it hits other flights
		self.cool_down()
		for laser in self.lasers:
			laser.move(velocity)
			if laser.off_screen(height):
				self.lasers.remove(laser)
			elif laser.collision(object):
				object.health = object.health - 10
				self.lasers.remove(laser)

	def draw(self, WINDOW): # Draw method, aims to draw the player ship onto the game window 
		WINDOW.blit(self.ship_image, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(WINDOW)

	def get_height(self): # aims to obtain the height value (piexel) of the ship image
		return self.ship_image.get_height()

	def get_width(self): # aims to obtain the width value (pixel) of the ship image
		return self.ship_image.get_width()

class Player(Ship):
	def __init__(self, x, y, health=100): # Define the properties of the Player class
		super().__init__(x, y, health)
		self.ship_image = player_ship
		self.laser_image = player_laser
		self.mask = pygame.mask.from_surface(self.ship_image)
		self.max_health = health

	def move_lasers(self, velocity, objects): # Move_lasers method, aims to check whether the laser fired by the player goes beyond the window or hits other flights
		self.cool_down()
		for laser in self.lasers:
			laser.move(velocity)
			if laser.off_screen(height):
				self.lasers.remove(laser)
			else:
				for object in objects:
					if laser.collision(object):
						objects.remove(object)
						if laser in self.lasers:
							self.lasers.remove(laser)

	def health_bar(self, WINDOW): # Health_bar method, aims to specified how the health bar of the player ship is drawed
		pygame.draw.rect(WINDOW, (255,0,0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width(), 15)) # rectangle, red
		pygame.draw.rect(WINDOW, (0,255,0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width()*(self.health/self.max_health), 15)) # rectangle, green

	def draw(self, WINDOW): # Draw method, aims to draw the health bar of the player ship
		super().draw(WINDOW)
		self.health_bar(WINDOW)

class Enemy(Ship):
	color_map = {"white": (white_ship, red_laser), 
				"blue": (blue_ship, green_laser), 
				"yellow": (yellow_ship, blue_laser)} ### In this game, we just create 3 kinds of enemy ship, denoted as the "white_ship", "blue_ship" and "yellow_ship"

	def __init__(self, x, y, color, health=100): # Define the properties of the Enemy class
		super().__init__(x, y, health)
		self.ship_image, self.laser_image = self.color_map[color]
		self.mask = pygame.mask.from_surface(self.ship_image)

	def move(self, velocity):
		self.y = self.y + velocity

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_image)
			self.lasers.append(laser)
			self.cool_down_counter += 1


def collide(object1, object2):
	offset_x = int(object2.x - object1.x)
	offset_y = int(object2.y - object1.y)
	return object1.mask.overlap(object2.mask, (offset_x, offset_y))


def main(): # This is the main game function. If wanting to start the game, call main()

	run = True # Decides whether the proceed the game
	lost = False # Set "lost" to False at the beginning, otherwise the game cannot start
	restart = False
	FPS = 60 # Frame-Per-Second, the rate of the game to be running
	lost_wait_time = 3 # Specifies the length of the waiting time (in [second]) before the game restart after the player loses the game


	level = 1 # Indicates the current game level
	lives = 5 # Indicates the number of lives remaining
	lost_time_counter = 0 # Keeps track of how long the player has waited after he/she lost
	

	enemies = []
	enemy_wave_number = 3 # Initial number of enemies at the initial level of the game 
	enemy_shoot_period = 4 # Specifies the average time interval (in [second]) between consecutive enemy shooting
	enemy_velocity = 2 # Velocity of the enemy ship
	player_velocity = 8 # Velocity of the player ship
	enemy_laser_velocity = 3 # Velocity of the enemy laser
	player_laser_velocity = -5 # Velocity of the player laser


	game_font = pygame.font.SysFont("comicsans", 50) # This specifies the font and size of the text label in the game
	lost_font = pygame.font.SysFont("comicsans", 70)

	player = Player(0.45*width, 0.85*height) # This specifies the initial position of the player ship at the moment when the game starts

	clock = pygame.time.Clock()


	def update_window():
		WINDOW.blit(background, (0,0)) # Took the background image, and draw it at coordinate (0,0) on the game WINDOW
		
		# Below update and draw the text labels on the game window:
		level_label = game_font.render("Level: " + str(level), 1, (255,0,0)) # Update the text level label on the game window
		lives_label = game_font.render("Lives: " + str(lives), 1, (0,255,0)) # Update the text lives label on the game window
		WINDOW.blit(level_label, (10,10)) # Draw the level label on the game window
		WINDOW.blit(lives_label, (width - level_label.get_width() - 10, 10)) # Draw the lives label

		player.draw(WINDOW) # Draw the player ship on the window

		if lost: # Condition triggered after the player lost the game
			lost_label = lost_font.render("You Have Lost!", 1, (255,255,255))
			WINDOW.blit(lost_label, (width/2 - lost_label.get_width()/2, height/2 - lost_label.get_height()/2))

		for enemy in enemies:
			  enemy.draw(WINDOW) # Draw all the enemy ships on the game window

		pygame.display.update()


	while run:
		clock.tick(FPS) # Tick the clock with the rate specified by "FPS"

		if restart:
			break

		if lives <= 0 or player.health <= 0: # Check whether the player has lost or not
			lost = True
			lost_time_counter = lost_time_counter + 1

		if lost and (lost_time_counter >= FPS * lost_wait_time): # After lost the game and waiting for lost_wait_time, stop the game
			run = False


		if len(enemies) == 0: # If eliminated all the enemy in the current level, increment the level and add more enemies, which increases the difficulty
			level = level + 1
			enemy_wave_number = enemy_wave_number + 5
			for i in range(enemy_wave_number):
				enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), random.choice(["white","yellow","blue"])) # Generate randomized enemy
				enemies.append(enemy) # add newly generated enemy into enemy record


		for event in pygame.event.get():
			if event.type == pygame.QUIT:  ### This is the way to stop and quit the game
				run = False

		# Below specifies the control mechanism of the player ship
		key = pygame.key.get_pressed()
		if (key[pygame.K_a] or key[pygame.K_LEFT]) and (player.x - player_velocity >= 0): # "a" or "left" being pressed, move the ship left
			player.x = player.x - player_velocity
		if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (player.x + player.get_width() + player_velocity <= width): # "d" or "right" being pressed, move the ship right
			player.x = player.x + player_velocity
		if (key[pygame.K_w] or key[pygame.K_UP]) and (player.y - player_velocity >= 0): # "w" or "up" being pressed, move the ship up
			player.y = player.y - player_velocity
		if (key[pygame.K_s] or key[pygame.K_DOWN]) and (player.y + player.get_height() + player_velocity <= height): # "s" or "down" being pressed, move the ship down
			player.y = player.y + player_velocity
		if key[pygame.K_SPACE]: # "Space" button being pressed, fire the laser bullet
			player.shoot()
		if key[pygame.K_p]:
			restart = not restart


		for enemy in enemies[:]: # Move each enemy and detects whether the laser bullet from each enemy goes beyond the window or hits the player ship
			enemy.move(enemy_velocity)
			enemy.move_lasers(enemy_laser_velocity, player)

			if random.randrange(0, enemy_shoot_period*FPS) == 10: # Tells the enemy ship when to fire a laser bullet
				enemy.shoot()

			if collide(enemy, player): # When the enemy ship collides with the player ship, deduct 10 health from the player ship and remove the enemy ship
				player.health = player.health - 10
				enemies.remove(enemy)
			elif enemy.y + enemy.get_height() >= height: # When the enemy ship reaches the bottom of the game window, deduct 1 life from the player and remove the enemy ship
				lives = lives - 1
				enemies.remove(enemy)

		player.move_lasers(player_laser_velocity, enemies) # The player fires laser that moves upward, therefore use "-laser_velocity"

		update_window()


def main_menu(): # Define the main menu program
	title_font = pygame.font.SysFont("comicsans", 70)
	run = True

	while run:
		WINDOW.blit(background, (0,0))
		title_label = title_font.render("Press the mouse to begin", 1, (255,255,255)) # Setup the title label before the game starts
		WINDOW.blit(title_label, (width/2 - title_label.get_width()/2, height/2)) # Print the title game on the game window
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN: # If the mouse is pressed, start the game by calling the main game function "main()"
				main()

main_menu()