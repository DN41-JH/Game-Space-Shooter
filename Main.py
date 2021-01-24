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

class Laser:
	def __init__(self, x, y, image):
		self.x = x
		self.y = y
		self.image = image
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, WINDOW):
		window.blit(self.image, (self.x, self.y))

	def off_screen(self, height):
		return self.y <= height and self.y >=0

	def collision(self, object):
		return collide(object, self)


class Ship:
	CoolDown = 30

	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_image = None
		self.laser_image = None
		self.lasers = []
		self.cool_down_counter = 0

	def cool_down(self):
		if self.cool_down_counter >= self.CoolDown:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter = self.cool_down_counter + 1

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_image)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	def move_lasers(self, velocity, object):
		#self.CoolDown()

		for laser in self.lasers:
			laser.move(velocity)
			if laser.off_screen(height):
				self.lasers.remove(laser)
			elif laser.collision(object):
				object.health = object.health - 10
				self.lasers.remove(laser)


	def draw(self, WINDOW):
		WINDOW.blit(self.ship_image, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(WINDOW)

	def get_height(self):
		return self.ship_image.get_height()

	def get_width(self):
		return self.ship_image.get_width()

class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_image = player_ship
		self.laser_image = yellow_laser
		self.mask = pygame.mask.from_surface(self.ship_image)
		self.max_health = health

	def move_lasers(self, velocity, objects):
		#self.CoolDown()
		for laser in self.lasers:
			laser.move(velocity)
			if laser.off_screen(height):
				self.lasers.remove(laser)
			else:
				for object in objects:
					if laser.collision(object):
						objects.remove(object)
						self.lasers.remove(laser)




class Enemy(Ship):
	color_map = {"red": (red_ship, red_laser), 
				"green": (green_ship, green_laser), 
				"blue": (blue_ship, blue_laser)}

	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.ship_image, self.laser_image = self.color_map[color]
		self.mask = pygame.mask.from_surface(self.ship_image)

	#def move(self, velocity):
	#	self.y = self.y + velocity


def collide(object1, object2):
	offset_x = object2.x - object1.x
	offset_y = object2.y - object1.y
	return object1.mask.overlap(object2.mask, (offset_x, offset_y))


def main():
	run = True # Decides whether the proceed the game
	lost = False
	FPS = 60 # Frame-Per-Second, the rate of the game to be running
	lost_wait_time = 3


	level = 0 # Indicates the current game level
	lives = 5 # Indicates the number of lives remaining
	lost_time_counter = 0
	

	enemies = []
	wave_length = 5
	enemy_velocity = 3
	laser_velocity = 4
	player_velocity = 5


	game_font = pygame.font.SysFont("comicsans", 50) # This specifies the font and size of the text label in the game
	lost_font = pygame.font.SysFont("comicsans", 70)

	player = Player(0.45*width, 0.6*height)



	clock = pygame.time.Clock()

	def update_window():
		WINDOW.blit(background_black, (0,0)) # Took the background_black image, and draw it at coordinate (0,0) on the game WINDOW
		
		# Below update and draw the text labels on the game window:
		level_label = game_font.render("Level: " + str(level), 1, (255,0,0)) # Update the text level label on the game window
		lives_label = game_font.render("Lives: " + str(lives), 1, (0,255,0)) # Update the text lives label on the game window
		WINDOW.blit(level_label, (10,10))
		WINDOW.blit(lives_label, (width - level_label.get_width() - 10, 10))


		player.draw(WINDOW)

		if lost:
			lost_label = lost_font.render("You Have Lost!", 1, (255,255,255))
			WINDOW.blit(lost_label, (width/2 - lost_label.get_width()/2, height/2 - lost_label.get_height()/2))

		for enemy in enemies:
			  enemy.draw(WINDOW)


		pygame.display.update()


	while run:
		clock.tick(FPS) # Tick the clock with the rate specified by "FPS"

		if lives <= 0 or player.health <= 0:
			lost = True
			lost_time_counter = lost_time_counter + 1

		if lost and (lost_time_counter >= FPS * lost_wait_time):
			run = False


		if len(enemies) == 0:
			level = level + 1
			wave_length = wave_length + 5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), random.choice(["red","blue","green"]))
				enemies.append(enemy)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:  ### This is the way to stop and quit the game
				run = False

		key = pygame.key.get_pressed()
		if (key[pygame.K_a] or key[pygame.K_LEFT]) and (player.x - player_velocity >= 0): # "a" or "left" being pressed, move the ship left
			player.x = player.x - player_velocity
		if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (player.x + player.get_width() + player_velocity <= width): # "d" or "right" being pressed, move the ship right
			player.x = player.x + player_velocity
		if (key[pygame.K_w] or key[pygame.K_UP]) and (player.y - player_velocity >= 0): # "w" or "up" being pressed, move the ship up
			player.y = player.y - player_velocity
		if (key[pygame.K_s] or key[pygame.K_DOWN]) and (player.y + player.get_height() + player_velocity <= height): # "s" or "down" being pressed, move the ship down
			player.y = player.y + player_velocity

		if key[pygame.K_SPACE]:
			player.shoot()



		for enemy in enemies[:]:
			#enemy.move(enemy_velocity)
			enemy.y = enemy.y + enemy_velocity
			enemy.move_lasers(laser_velocity, player)
			if enemy.y + enemy.get_height() >= height:
				lives = lives - 1
				enemies.remove(enemy)

		player.move_lasers(laser_velocity, enemies)

		update_window()


main()