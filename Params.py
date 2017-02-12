import math
from Renderer import Renderer

num_inputs = 4
num_hidden_layers = 1
neurons_per_hidden_layer = 3
num_outputs = 5
bias = -1
activation_response = 1

# Note this is size for each population. Therefore total Entities = population_size * 2
population_size = 20

mutation_rate = 0.3
mutation_power = 0.45
crossover_rate = 0
MAX_TURN_RATE = 40
MAX_TICKS = 1200
TEAM_ONE_SPAWN = (325, 250)
TEAM_TWO_SPAWN = (Renderer.SCREEN_WIDTH - 325, Renderer.SCREEN_HEIGHT - 300)
FITNESS_FOR_WIN = 3
FITNESS_FOR_HIT = 0
FITNESS_FOR_DRAW = 1
FITNESS_FOR_LOSS = 0
FIGHTER_HEALTH = 3
MATCHES_PER_FIGHTER = 5
TOTAL_ROUNDS = population_size * MATCHES_PER_FIGHTER
FIRE_RATE = 1
MIN_FOV_ANGLE = 5
MAX_FOV_ANGLE = 85
FOV_DISTANCE = 400
FOV_CHANGE_PER_FRAME = 0.5
