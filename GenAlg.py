from NeuralNets import Neuron
from NeuralNets import NeuronLayer
from NeuralNets import NeuralNet
from Entity import Entity
import math
import Params
import random

NUM_BEST_CHOSEN = 0
NUM_BEST_COPIES = 0

old_pop = []
new_pop = []
total_fitness = 0
average_fitness = 0

def get_total_fitness():
    global total_fitness

    for entity in old_pop:
        total_fitness += entity.fitness


def get_avg_fitness():
    global average_fitness
    tot_fitness = 0
    for i in range(len(old_pop)):
        tot_fitness += old_pop[i].fitness

    average_fitness = tot_fitness / len(old_pop)


def sort_entities(entities):
    i = len(entities) - 1

    while i >= 0:
        j = 0
        while j < i:
            first_fitness = entities[j].fitness
            second_fitness = entities[j + 1].fitness

            if first_fitness < second_fitness:
                temp = entities[j + 1]
                entities[j + 1] = entities[j]
                entities[j] = temp
            j += 1
        i -= 1

    return entities


def copy_best():
    global new_pop

    for i in range(NUM_BEST_CHOSEN):
        for j in range(NUM_BEST_COPIES):
            new_entity = Entity()
            new_entity.brain.replace_weights(old_pop[i].brain.get_weights())
            new_pop.append(new_entity)


# Picks a random number between 0 and the fitness of the population.
# Loops through each index, subtracting the fitness of each entity from the threshold.
# When the threshold reaches zero, the current index is chosen as the parent.
# This method gives fitter individuals a higher chance to be selected,
# but does not guarantee the selection of any particular individual.
def get_parent():
    global old_pop

    selection_threshold = random.uniform(0, total_fitness)
    cur_selection = 0

    while selection_threshold > cur_selection:
        selection_threshold -= old_pop[cur_selection].fitness
        cur_selection += 1

    #print("Average: " + str(average_fitness) + " Actual: " + str(old_pop[cur_selection - 1].fitness))

    return old_pop[cur_selection - 1]


def crossover(mum, dad):
    # Copy parents if crossover rate doesn't pass,
    # or if same parent was selected as both mum and dad.
    if random.uniform(0, 1) < Params.crossover_rate or mum == dad:
        child_one = Entity()
        child_two = Entity()
        child_one.brain.replace_weights(mum.brain.get_weights())
        child_two.brain.replace_weights(dad.brain.get_weights())

        return child_one, child_two

    # If crossover happens, randomly select each weight from either mum or dad
    #parent_weights = (mum.brain.get_weights(), dad.brain.get_weights())

    child_one = Entity()
    child_two = Entity()

    child_one_weights = []
    child_two_weights = []

    # Determine crossover point
    # crossover_point = random.randint(0, mum.brain.get_number_of_weights() - 1)

    swap_crossover = False

    # For each layer
    for i in range(Params.num_hidden_layers + 1):
        # For each neuron
        for j in range(mum.brain.layers[i].num_neurons):
            # Crossover for each neuron. Children cris-cross for each neuron between parents.
            swap_crossover = not swap_crossover

            # For each weight
            for k in range(mum.brain.layers[i].neurons[j].num_inputs):
                if swap_crossover:
                    child_one_weights.append(mum.brain.layers[i].neurons[j].input_weights[k])
                    child_two_weights.append(dad.brain.layers[i].neurons[j].input_weights[k])
                else:
                    child_one_weights.append(dad.brain.layers[i].neurons[j].input_weights[k])
                    child_two_weights.append(mum.brain.layers[i].neurons[j].input_weights[k])

    # Put the weights into the children
    child_one.brain.replace_weights(child_one_weights)
    child_two.brain.replace_weights(child_two_weights)

    return child_one, child_two





    # Assign each child a parent to copy weights from.
    # Copy weights from 0 -> crossover_point
    #for i in range(crossover_point):
        #child_one_weights.append(parent_weights[0][i])
        #child_two_weights.append(parent_weights[1][i])

    # Swap the parent the child copies weights from.
    # Copy weights from crossover_point -> end of list
    # for i in range(crossover_point, mum.brain.get_number_of_weights()):
    #     child_one_weights.append(parent_weights[1][i])
    #     child_two_weights.append(parent_weights[0][i])
    #
    # child_one.brain.replace_weights(child_one_weights)
    # child_two.brain.replace_weights(child_two_weights)
    #
    # return child_one, child_two


def mutate(entity):
    weights = entity.brain.get_weights()

    for weight in weights:
        if random.uniform(0, 1) > Params.mutation_rate:
            weight += Params.mutation_power * random.uniform(-1, 1)

    entity.brain.replace_weights(weights)


def evolve(population):
    global old_pop
    global new_pop
    old_pop = population
    new_pop = []

    global total_fitness
    total_fitness = 0

    global average_fitness
    average_fitness = 0

    # Sort old population by fitness
    old_pop = sort_entities(old_pop)

    # Remove lowest fitness from old population
    old_pop.pop(len(old_pop) - 1)

    get_total_fitness()
    #get_avg_fitness()

    # Add elite entities to new population
    copy_best()

    # Continue generating new entities until new population is filled
    while len(new_pop) < Params.population_size:
        # Select parents
        mum = get_parent()
        dad = get_parent()

        # Create 2 children and mutate them
        children = crossover(mum, dad)
        mutate(children[0])
        mutate(children[1])

        # Add new children to population
        new_pop.append(children[0])
        new_pop.append(children[1])

    # Population has been refilled, return
    return new_pop
