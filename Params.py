import math
from Renderer import Renderer

num_inputs = 7
num_hidden_layers = 2
neurons_per_hidden_layer = 5
num_outputs = 3
bias = -1
activation_response = 1
population_size = 30
num_food = 60
num_ponds = 2
mutation_rate = 0.3
mutation_power = 0.3
crossover_rate = 0
MAX_TURN_RATE = 179
MAX_TICKS = 600
TEAM_ONE_SPAWN = (100, 100)
TEAM_TWO_SPAWN = (Renderer.SCREEN_WIDTH - 100, Renderer.SCREEN_HEIGHT - 100)
FITNESS_FOR_WIN = 3
FITNESS_FOR_DRAW = 1
FITNESS_FOR_LOSS = 0
FIGHTER_HEALTH = 3
