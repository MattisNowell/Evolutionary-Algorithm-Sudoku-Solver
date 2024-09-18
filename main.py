from copy import deepcopy
import time
import random
from random import choice
import Sudoku

sudoku_range = (1,2,3,4,5,6,7,8,9)

## INITIATION FUNCTIONS

def initialise(sudoku:list) -> list:
    """Randomly populates all blank tiles of a sudoku with random numbers."""
    return [choice(sudoku_range) if type(number) == int and number == 0 else number for number in sudoku]

## REPRODUCTION FUNCTIONS

def crossover(sudoku_x:list, sudoku_y:list) -> list:
    """Combines two sudoku boards into one child board based on randomness of selection."""
    # If the difference between sudoku_x and sudoku_y is of two or less values, let the child be randomised from scrap to ensure genetic diversity:
    if len(diff(sudoku_x, sudoku_y)) <= 2:
        return initialise(base_sudoku)
    # Else let the child be a randomised combination of the two sudokus
    else:
        return [(choice(pair)) for pair in list(zip(sudoku_x, sudoku_y)) ] 

def mutate(sudoku:list) -> list:
    """Takes a sudoku and produces a mutated version of the configuration with a chance of having modified values depending on the mutation rate."""
    return [ choice(sudoku_range) if type(number) == int and random.random() < MUTATION_RATE else number for number in sudoku ]
            

## SELECTION FUNCTIONS

def fitness(sudoku:list) -> int:
    """Evaluates a given sudoku configuration through an integer value."""
    evaluation:int = 0
    # For each sub-structure contained in a sudoku board:
    for i in range(0,9):
        # And for each number a sub-structure should have:
        for number in sudoku_range:
            # Check if the number is contained in the column:
            if number not in column(sudoku, i):
                evaluation += 1
            # Check if the number is contained in the row:
            if number not in row(sudoku, i):
                evaluation += 1
            # Check if the number is contained in the grid:
            if number not in grid(sudoku, i):
                evaluation += 1
    return evaluation

def select(sudoku_list:list, sudoku_evaluation:list) -> list:
    """Returns the top fittest sudoku boards from a generation."""
    sorted_population = sorted(zip(sudoku_list, sudoku_evaluation), key = lambda eval: eval[1])
    selected:list = []
    for sudoku in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)]:
        if random.randint(0,9) == 5:
            selected.append(choice(sorted_population))
        else:
            selected.append(sudoku)
    return selected

def fittest(sudoku_list:list, sudoku_evaluation:list) -> list:
    """Returns the fittest sudoku board from a generation."""
    return sorted(zip(sudoku_list, sudoku_evaluation), key = lambda eval: eval[1])[0]

if __name__ == "__main__":

    print(len(SUDOKU_ONE))
     
    generation:list = []
    evaluations:list = []

    # Initialising the population and their fitness:
    for _ in range(POPULATION_SIZE):
        child = initialise(base_sudoku)
        generation.append(child)
        evaluations.append(fitness(toint(child)))

    increment = 0
    beginning = time.time()
    while True:
        increment += 1
        sorted_population = sorted(zip(generation, evaluations), key = lambda eval: eval[1])
        for i in range(len(sorted_population)-POPULATION_SIZE):
            sorted_population.pop()
        generation = [ individual[0] for individual in sorted_population ]
        evaluations = [ individual[1] for individual in sorted_population ]

        # Selecting the best individuals of the current generation:
        selection:list = select(generation, evaluations)
        generation = []
        evaluations = []
        # Reproduction:
        for _ in range(POPULATION_SIZE):
            # Selecting non-equal parents from the best individuals:
            parentA = choice(selection)
            parentB = []
            while parentB == [] or parentB == parentA:
                parentB = choice(selection)
            # Creating a child by crossing over the selected parents:
            child = crossover(parentA[0], parentB[0]) 
            # Mutating the child:
            child = mutate(child)
            # Adding the resulting child to the new generation's list and computing and storing the child's fitness:
            generation.append(child)              
            evaluations.append(fitness(toint(child))  )
        # Select the fittest individual of the new established generation:
        best = fittest(generation, evaluations)
        # Printing execution and fittest values:
        print(best[1])
        print(increment)
        # If the board has achieved its goal or the number of authorized generations has been reached, terminate the program:
        if best[1] == 0 or increment == NUMBER_GENERATION:
            display(best[1])
            break
    print(time.time() - beginning)