from sudoku import Sudoku
from copy import deepcopy
import time
import random
from random import choice

class Evolutionary:
    individual_size = 81

    def __init__(self, sudoku:Sudoku, config_path:str="config.txt"):
        """"""
        self.sudoku = sudoku
        self.get_config(config_path)
    
    # TECHNICAL METHODS
    def get_config(self, path:str) -> None:
        """"""
        with open(path, "rt") as config:
            line = config.readline()
            self.number_generation = int(line[line.index('=')+1::])
            line = config.readline()
            self.population_size = int(line[line.index('=')+1::])
            line = config.readline()
            self.truncation_rate = float(line[line.index('=')+1::])
            line = config.readline()
            self.mutation_rate = (1/81) * int(line[line.index('=')+1::])

    # INDIVIDUAL LEVEL METHODS
    def initialise(self) -> Sudoku:
        """Randomly populates all blank tiles of a sudoku with random numbers."""
        return Sudoku(layout=[choice(Sudoku.INT_RANGE) if type(number) == int and number == 0 else number for number in self.sudoku.layout])
    
    # REDOOO
    def crossover(self, parent_sudoku_a:Sudoku, parent_sudoku_b:Sudoku) -> Sudoku:
        """Combines two sudoku boards into one child board based on randomness of selection."""
        if len(parent_sudoku_a.compare(parent_sudoku_b)) <= 2:
            return self.initialise()
        else:
            return Sudoku(layout=[(choice(pair)) for pair in list(zip(parent_sudoku_a.layout, parent_sudoku_b.layout))])
        
    # REDOOO
    def mutate(self, sudoku:Sudoku) -> Sudoku:
        """Takes a sudoku and produces a mutated version of the configuration with a chance of having modified values 
        depending on the mutation rate."""
        return Sudoku(layout=[choice(Sudoku.INT_RANGE) if type(number) == int and random.random() < self.mutation_rate else number for number in sudoku.layout])
    
    # GENERATION LEVEL METHODS
    
    # REDOOO
    def select(self, generation:list[Sudoku]) -> list[Sudoku]:
        """Returns the top fittest sudoku boards from a generation."""
        selection = []
        for sud in range(self.population_size):
            tournament = []
            for i in range(3):
                tournament.append(choice(generation))
            tournament.sort(key= lambda x: x.fitness)
            selection.append(tournament[0])
        return selection

        #sorted_population = sorted(generation, key = lambda x: x.fitness)
        #truncation_threshold = int(self.population_size*self.truncation_rate)
        #return [choice(sorted_population[truncation_threshold:]) if random.randint(0,2) == 2 else sudoku for sudoku in sorted_population[:truncation_threshold]]

    @staticmethod
    def fittest(generation:list) -> Sudoku:
        """Returns the fittest sudoku board from a generation."""
        return sorted(generation, key = lambda x: x.fitness)[0]
    
    # EXECUTION 

    def solve(self) -> float:
        """
        """
        generation = []
        # Initialising the population:
        for _ in range(self.population_size):
            generation.append(self.initialise())
        increment = 0
        beginning = time.time()
        while True:
            increment += 1
            # Selecting the best individuals of the current generation:
            selection = self.select(generation)
            generation = []
            for _ in range(self.population_size):
                # Selection:
                parentA = choice(selection)
                parentB = choice(selection)
                while parentB.layout == parentA.layout:
                    parentB = choice(selection)
                # Crossover:
                child = self.crossover(parentA, parentB) 
                # Mutation:
                child = self.mutate(child)
                generation.append(child)                          
            fittest = self.fittest(generation)
            print("\nGeneration number " + str(increment) + ": ")
            print(str(fittest.fitness))
            if fittest.fitness == 0 or increment == self.number_generation:
               print(fittest.display())
               break
        print(time.time() - beginning)

#s = Sudoku(path="sample_sudoku_1.txt")
s = Sudoku(layout=['3',0,0,0,0,'5',0,'4','7',
0,0,'6',0,'4','2',0,0,'1',
0,0,0,0,0,'7','8','9',0,
0,'5',0,0,'1','6',0,0,'2',
0,0,'3',0,0,0,0,0,'4',
'8','1',0,0,0,0,'7',0,0,
0,0,'2',0,0,0,'4',0,0,
'5','6',0,'8','7',0,'1',0,0,
0,0,0,'3',0,0,'6',0,0])
solver = Evolutionary(s)
print(solver.sudoku.display())
solver.solve()