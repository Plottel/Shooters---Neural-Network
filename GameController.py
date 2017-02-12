import math
import random
import time
import pygame
import pygame.font
import Params
import random
import Input
from Entity import Entity
from NeuralNets import NeuralNet
import Utils
from Renderer import Renderer
import GenAlg

SKIP_GENERATION = False
SKIP_ROUND = False
GENERATION_IN_PROGRESS = True

start_time = time.time()
CURRENT_GENERATION = 1
CURRENT_ROUND = 0
CURRENT_TICK = 0

pop_one = []
pop_two = []
pop_one_fight_sequence = []
pop_two_fight_sequence = []

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 15)

# Create random brains for first generation
def init():
    # Create entities
    for i in range(Params.population_size):
        ent_one = Entity()
        ent_one.x = Params.TEAM_ONE_SPAWN[0]
        ent_one.y = Params.TEAM_ONE_SPAWN[1]
        pop_one.append(ent_one)

        ent_two = Entity()
        ent_two.x = Params.TEAM_TWO_SPAWN[0]
        ent_two.y = Params.TEAM_TWO_SPAWN[1]
        pop_two.append(ent_two)

    # Determine fight sequence
    global pop_one_fight_sequence
    global pop_two_fight_sequence

    for i in range(Params.population_size):
        for j in range(Params.MATCHES_PER_FIGHTER):
            pop_one_fight_sequence.append(i)
            pop_two_fight_sequence.append(i)

    random.shuffle(pop_one_fight_sequence)
    random.shuffle(pop_two_fight_sequence)


def render():
    pop_one[pop_one_fight_sequence[CURRENT_ROUND]].render()
    pop_two[pop_two_fight_sequence[CURRENT_ROUND]].render()

    Renderer.SCREEN.blit(FONT.render("Generation: " + str(CURRENT_GENERATION), 1, (0, 0, 0)), (10, 10))
    Renderer.SCREEN.blit(FONT.render("Round: " + str(CURRENT_ROUND), 1, (0, 0, 0)), (10, 30))
    Renderer.SCREEN.blit(FONT.render("Tick: " + str(CURRENT_TICK), 1, (0, 0, 0)), (10, 50))


# DOES NOT RESET FITNESS
def reset_entity(entity, team):
    if team == 1:
        entity.x = Params.TEAM_ONE_SPAWN[0]
        entity.y = Params.TEAM_ONE_SPAWN[1]
    else:
        entity.x = Params.TEAM_TWO_SPAWN[0]
        entity.y = Params.TEAM_TWO_SPAWN[1]

    entity.heading = 0
    entity.change_angle(0)
    entity.health = Params.FIGHTER_HEALTH
    entity.last_shot_at = 0


def reset_population():
    global pop_one
    global pop_two

    for i in range(Params.population_size):
        reset_entity(pop_one[i], 1)
        reset_entity(pop_two[i], 2)

        # Fitness reset manually because reset entity does not reset fitness.
        # This is to allow resetting between rounds since an entity fights multiple rounds.
        pop_one[i].fitness = 0
        pop_two[i].fitness = 0


def get_inputs(to_get, enemy):
    to_get.can_see_enemy = int(Utils.rect_tri_intersect(enemy.rect, to_get.fov_triangle))

    if enemy.bullet is None:
        to_get.can_see_bullet = int(False)
    else:
        to_get.can_see_bullet = int(Utils.rect_tri_intersect(enemy.bullet.rect, to_get.fov_triangle))

    max_change = Params.MAX_FOV_ANGLE - Params.MIN_FOV_ANGLE
    current_change_from_min = to_get.fov_angle - Params.MIN_FOV_ANGLE

    fov_as_pcnt_of_max = current_change_from_min / max_change

    return [
        to_get.can_see_enemy,
        to_get.can_see_bullet,
        int(to_get.can_shoot()),
        fov_as_pcnt_of_max
    ]


def fight_over(ftr_one, ftr_two):
    # Check if the round is over
    # Time up
    if CURRENT_TICK > Params.MAX_TICKS:
        # Draw
        if ftr_one.health == ftr_two.health:
            # If nobody hit anything, they don't get the draw fitness bonus
            if ftr_one.health == Params.FIGHTER_HEALTH and ftr_two.health == Params.FIGHTER_HEALTH:
                ftr_one.fitness += Params.FITNESS_FOR_LOSS
                ftr_two.fitness += Params.FITNESS_FOR_LOSS
            else:
                ftr_one.fitness += Params.FITNESS_FOR_DRAW
                ftr_two.fitness += Params.FITNESS_FOR_DRAW
        # Fighter one wins
        elif ftr_one.health > ftr_two.health:
            ftr_one.fitness += Params.FITNESS_FOR_WIN
            ftr_two.fitness += Params.FITNESS_FOR_LOSS
        # Fighter two wins
        elif ftr_two.health > ftr_one.health:
            ftr_one.fitness += Params.FITNESS_FOR_LOSS
            ftr_two.fitness += Params.FITNESS_FOR_WIN
        return True
    # Draw
    elif ftr_one.health == 0 and ftr_two.health == 0:
        ftr_one.fitness += Params.FITNESS_FOR_DRAW
        ftr_two.fitness += Params.FITNESS_FOR_DRAW
        return True
    # Fighter two wins
    elif ftr_one.health == 0:
        ftr_one.fitness += Params.FITNESS_FOR_LOSS
        ftr_two.fitness += Params.FITNESS_FOR_WIN
        return True
    # Fighter one wins
    elif ftr_two.health == 0:
        ftr_one.fitness += Params.FITNESS_FOR_WIN
        ftr_two.fitness += Params.FITNESS_FOR_LOSS
        return True

    return False


def fight(ftr_one, ftr_two):
    # Get inputs
    inputs_one = get_inputs(ftr_one, ftr_two)
    inputs_two = get_inputs(ftr_two, ftr_one)

    # Get outputs
    outputs_one = ftr_one.brain.update(inputs_one)
    outputs_two = ftr_two.brain.update(inputs_two)

    # Process outputs
    ftr_one.handle_outputs(outputs_one)
    ftr_two.handle_outputs(outputs_two)

    # Move fighters
    ftr_one.move()
    ftr_two.move()

    # Handle bullet collisions
    if ftr_one.hit_target(ftr_two):
        ftr_two.health -= 1
        ftr_one.fitness += Params.FITNESS_FOR_HIT

    if ftr_two.hit_target(ftr_one):
        ftr_one.health -= 1
        ftr_one.fitness += Params.FITNESS_FOR_HIT

    # Check if round is over
    if fight_over(ftr_one, ftr_two):
        reset_entity(ftr_one, 1)
        reset_entity(ftr_two, 2)

        global CURRENT_ROUND
        CURRENT_ROUND += 1

        global CURRENT_TICK
        CURRENT_TICK = 0


def tick():
    global CURRENT_TICK
    CURRENT_TICK += 1
    fight(pop_one[pop_one_fight_sequence[CURRENT_ROUND]], pop_two[pop_two_fight_sequence[CURRENT_ROUND]])


def evolve():
    global pop_one
    global pop_two

    print("Current Generation: " + str(CURRENT_GENERATION))

    global CURRENT_GENERATION
    CURRENT_GENERATION += 1

    global CURRENT_TICK
    CURRENT_TICK = 0

    global CURRENT_ROUND
    CURRENT_ROUND = 0

    # Evolve 2 generations together
    new_generation = GenAlg.evolve(pop_one + pop_two)
    random.shuffle(new_generation)

    # Redistribute into 2 generations
    pop_one = []
    pop_two = []

    for i in range(Params.population_size):
        pop_one.append(new_generation.pop(len(new_generation) - 1))
        pop_two.append(new_generation.pop(len(new_generation) - 1))

    reset_population()

    random.shuffle(pop_one_fight_sequence)
    random.shuffle(pop_two_fight_sequence)

# Runs one tick if set to normal speed.
# Fast-forwards according to SKIP_GENERATION and SKIP_ROUND variables
def run():
    global SKIP_GENERATION
    global SKIP_ROUND

    if Input.key_typed(pygame.K_s):
        SKIP_GENERATION = not SKIP_GENERATION

    if Input.key_typed(pygame.K_r):
        SKIP_ROUND = True

    if not SKIP_GENERATION and not SKIP_ROUND:
        if CURRENT_ROUND > Params.TOTAL_ROUNDS:
            evolve()

        tick()
        render()
    elif SKIP_GENERATION:
        while CURRENT_ROUND < Params.TOTAL_ROUNDS:
            tick()
            Input.process_events()
            if Input.key_typed(pygame.K_s):
                SKIP_GENERATION = False
                break

        if CURRENT_ROUND == Params.TOTAL_ROUNDS:
            evolve()
    elif SKIP_ROUND:
        next_round = CURRENT_ROUND + 1
        while CURRENT_ROUND is not next_round:
            tick()
        SKIP_ROUND = False


