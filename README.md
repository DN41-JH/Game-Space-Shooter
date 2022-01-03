# Game: Shooting Space Ships

This is a game that allows a single player to control his/her own space ship that is able to emit laser bullet to attack randomly emerging enemy ships from the top of the game window. Feel free the customize the game (i.e. change the background image, adjust the space craft speed, etc.) inside the source code file (which is Main.py).

Run Main.py to start playing.

# Implementation Prerequisites

Before running the game, please make sure to have "pygame" package installed (https://www.pygame.org/download.shtml, or type "pip install pygame").

# Introduction

Start the Game: Click the mouse

Restart the Game: "R"

Movement: "W", "A", "S", "D", or "Up", "Left", "Down", "Right"

Shoot Lasers: "Space"

In order to keep playing, the player needs to destroy all the enemy ships before any of them reaches to the bottom of the game window, while maintaining a non-zero health. The player's health is reduced by 10 (with the maximum health to be 100 by default) each time the player is hit by an enemy laser. Once an enemy space ship reaches to the bottom of the game window, the remaining number of lives will be reduced by one. The game ends at the time when the player's health comes to 0 or 5 enemy ships have ever reached the bottom of the game window. When the player survives from the current wave of enemy, the diffculty level will be incremented by one, as more enemy ships will show up in the next wave.

# Demo:
A demo of the game program is available at: https://youtu.be/-41YESkrunI.
