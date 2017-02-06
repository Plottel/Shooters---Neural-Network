import math
import random
import time
import pygame
import Params
import Input
from Entity import Entity
from NeuralNets import NeuralNet

from Renderer import Renderer

import GenAlg

FAST_FORWARD = False
GENERATION_IN_PROGRESS = True

start_time = time.time()
CURRENT_GENERATION = 1
CUR_FTR = 0
CURRENT_TICK = 0

pop_one = []
pop_two = []

# Create random brains for first generation
def init():
    for i in range(Params.population_size):
        ent_one = Entity()
        ent_one.brain = NeuralNet()
        ent_one.x = Params.TEAM_ONE_SPAWN[0]
        ent_one.y = Params.TEAM_ONE_SPAWN[1]
        pop_one.append(ent_one)

        ent_two = Entity()
        ent_two.brain = NeuralNet()
        ent_two.x = Params.TEAM_TWO_SPAWN[0]
        ent_two.y = Params.TEAM_TWO_SPAWN[1]
        pop_two.append(ent_two)


def render():
    pop_one[CUR_FTR].render()
    pop_two[CUR_FTR].render()

def reset_population():
    global pop_one
    for entity in pop_one:
        entity.x = Params.TEAM_ONE_SPAWN[0]
        entity.y = Params.TEAM_ONE_SPAWN[1]
        entity.fitness = 0
        entity.heading = 0
        entity.change_angle(0)
        entity.health = Params.FIGHTER_HEALTH

    global pop_two
    for entity in pop_two:
        entity.x = Params.TEAM_TWO_SPAWN[0]
        entity.y = Params.TEAM_TWO_SPAWN[1]
        entity.fitness = 0
        entity.heading = 0
        entity.change_angle(0)
        entity.health = Params.FIGHTER_HEALTH


def get_inputs(to_get, enemy):
    inputs = []

    # Current facing
    inputs.append(to_get.dx)
    inputs.append(to_get.dy)

    # Required facing to face enemy
    to_get.get_vector_to_enemy(enemy)
    inputs.append(to_get.vector_to_enemy[0])
    inputs.append(to_get.vector_to_enemy[1])

    # Required vector to run into enemy bullet (i.e. avoid this)
    if enemy.bullet is None:
        inputs.append(0)
        inputs.append(0)
    else:
        to_get.get_vector_to_bullet(enemy.bullet)
        inputs.append(to_get.vector_to_bullet[0])
        inputs.append(to_get.vector_to_bullet[1])


    # Whether or not Entity has a current bullet on screen
    inputs.append(int(to_get.can_shoot()))

    return inputs


def tick():
    global CURRENT_TICK
    CURRENT_TICK += 1

    global pop_one
    global pop_two

    # Get inputs
    inputs_one = get_inputs(pop_one[CUR_FTR], pop_two[CUR_FTR])
    inputs_two = get_inputs(pop_two[CUR_FTR], pop_one[CUR_FTR])

    # Get outputs
    outputs_one = pop_one[CUR_FTR].brain.update(inputs_one)
    outputs_two = pop_two[CUR_FTR].brain.update(inputs_two)

    # Process outputs
    pop_one[CUR_FTR].handle_outputs(outputs_one)
    pop_two[CUR_FTR].handle_outputs(outputs_two)

    # Move fighters
    pop_one[CUR_FTR].move()
    pop_two[CUR_FTR].move()

    # Handle bullet collisions
    if pop_one[CUR_FTR].hit_target(pop_two[CUR_FTR]):
        pop_two[CUR_FTR].health -= 1

    if pop_two[CUR_FTR].hit_target(pop_one[CUR_FTR]):
        pop_one[CUR_FTR].health -= 1

    # Check if the round is over
    global CUR_FTR
    # Time up
    if CURRENT_TICK > Params.MAX_TICKS:
        pop_one[CUR_FTR].fitness = Params.FITNESS_FOR_DRAW
        pop_two[CUR_FTR].fitness = Params.FITNESS_FOR_DRAW

        global CURRENT_TICK
        CURRENT_TICK = 0
        CUR_FTR += 1
    # Draw
    elif pop_one[CUR_FTR].health == 0 and pop_two[CUR_FTR].health == 0:
        pop_one[CUR_FTR].fitness = Params.FITNESS_FOR_DRAW
        pop_two[CUR_FTR].fitness = Params.FITNESS_FOR_DRAW
        CUR_FTR += 1
    # Pop Two wins
    elif pop_one[CUR_FTR].health == 0:
        pop_one[CUR_FTR].fitness = Params.FITNESS_FOR_LOSS
        pop_two[CUR_FTR].fitness = Params.FITNESS_FOR_WIN
        CUR_FTR += 1
    # Pop One wins
    elif pop_two[CUR_FTR].health == 0:
        pop_one[CUR_FTR].fitness = Params.FITNESS_FOR_WIN
        pop_two[CUR_FTR].fitness = Params.FITNESS_FOR_LOSS
        CUR_FTR += 1


def evolve():
    global pop_one
    global pop_two

    print("Current Generation: " + str(CURRENT_GENERATION))

    global CURRENT_GENERATION
    CURRENT_GENERATION += 1

    global CURRENT_TICK
    CURRENT_TICK = 0

    global CUR_FTR
    CUR_FTR = 0

    pop_one = GenAlg.evolve(pop_one)
    pop_two = GenAlg.evolve(pop_two)

    reset_population()

def run():
    global FAST_FORWARD

    if Input.key_typed(pygame.K_s):
        FAST_FORWARD = not FAST_FORWARD

    if not FAST_FORWARD:
        if not CUR_FTR < Params.population_size - 1:
            evolve()

        tick()
        render()
    else:
        while CUR_FTR < Params.population_size - 1:
            tick()
        evolve()


