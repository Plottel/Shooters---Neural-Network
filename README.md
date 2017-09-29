# Shooters---Neural-Network

A program which teaches AIs to fight against each other using a simple 
feed-forward Neural Network. The network is trained by a Genetic Algorithm.

* Demo video - https://www.youtube.com/watch?v=afJB4jtnCaQ&t=7s
* Inspired by tutorials on http://www.ai-junkie.com/

### Simulation Specs
The program consists of two entities fighting against each other. They can move
around like a car (as though they had wheels - can only turn left / right) and are
able to shoot bullets with a two second cooldown. They also have a field of view
limited to a triangle in front of them. If their bullet collides with the enemy
fighter, an HP is deducted. 
Rounds are limited to 20 seconds and fighters each have 3 HP.

### Genetic Algorithm Specs
* __Population__ - Each fighter represents a population. The simulation has two populations evolving simultaneously.
* __Fitness__ - Each fighter competes in a number of rounds. Win = 3 fitness, Draw = 1 fitness, Loss = 0 fitness.
* __Parent Selection__ - Parents are selected using the "roulette wheel" method. If the same parent is selected twice, the process is repeated until two unique parents are found.
* __Crossover Operator__ - Crossover is performed using the Single-Point crossover method. The crossover
point is chosen randomly for each crossover operation.
* __Mutation Operator__ - Mutation is applied by manually adjusting the values of the weights by a clamped amount. A random number is rolled for each weight in the neural network. If this number surpasses the mutation rate, a second random number is rolled representing the adjustment value to apply to the weight.


### Neural Network Specs
* __Topology__ - A simple feed-forward network. 1 input layer (3 neurons), 1 hidden layer (4 neurons), 1 output layer (5 neurons).
* __Inputs__ * - All inputs are binary values. Can I see my enemy? Can I see a bullet? Is my shot off cooldown?
* __Outputs__ * - How far to turn left; how far to turn right; do I move at all?; do I shoot?; do I adjust my field of view?
