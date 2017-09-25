# Shooters---Neural-Network

A program which teaches AIs to fight against each other using a simple 
feed-forward Neural Network. The network is trained by a Genetic Algorithm.

* Demo video - https://www.youtube.com/watch?v=afJB4jtnCaQ&t=7s

### Simulation Specs
The program consists of two entities fighting against each other. They can move
around like a car (as though they had wheels - can only turn left / right) and are
able to shoot bullets with a two second cooldown. They also have a field of view
limited to a triangle in front of them. If their bullet collides with the enemy
fighter, an HP is deducted. 
Rounds are limited to 20 seconds and fighters each have 3 HP.

### Genetic Algorithm Specs
##### Population
Each fighter represents a population. The simulation has two populations evolving simultaneously.
