# Game: Shooting Space Ships

This is a game that allows a single player to control his/her own space ship that is able to emit laser bullet to attack randomly emerging enemy ships from the top of the game window. Before running the game, please make sure to have "pygame" package installed for Python. 

Run Main.py to start playing.

# Introduction

Movement: "W", "A", "S", "D", or "Up", "Left", "Down", "Right"

Shooting Lasers: "Space"

In order to keep playing, the player needs to destroy all the enemy ships before any of them reaches to the bottom of the game window, while maintaining a non-zero health. The player's health is reduced by 10 (with the maximum health to be 100 by default) each time the player is hit by an enemy laser. Once an enemy space ship reaches to the bottom of the game window, the remaining number of lives will be reduced by one. The game ends at the time when the player's health comes to 0 or 5 enemy ship has reached the bottom of the game window. When the player survives from the current wave of enemy, the diffculty level will be incremented by one, as more enemy ships will show up in the next wave.
