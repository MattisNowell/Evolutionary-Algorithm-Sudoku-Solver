## SUDOKU FUNCTIONS
class Sudoku:
    INT_RANGE = (1,2,3,4,5,6,7,8,9)

    def __init__(self, path:str="", layout=[]):
        if path != "":
            self.layout = self.read_file(path)
        else:
            self.layout = layout
        self.fitness = self.get_fitness()

    def grid(self, i:int):
        """Returns the data of the ith grid of a given sudoku board:"""
        if i in [0,1,2]:
            start = 0 + 3*i
        elif i in [3,4,5]:
            start = 27 + 3*(i-3)
        elif i in [6,7,8]:
            start = 54 + 3*(i-6)

        subgrid = []
        for o in range(0,3):
            for u in range(0,3):
                subgrid.append(self.layout[start+(o*9)+u])
        return subgrid

    def column(self, i:int):
        """Returns the data of the ith column of a given sudoku board.""" 
        return self.layout[i::9]

    def row(self, i:int):
        """Returns the data of the ith row of a given sudoku board.""" 
        return self.layout[i*9:i*9+9]

    def display(self) -> None:
        """Prints a board in a understandable way."""
        tostring:str = "" 
        for number in range(len(self.layout)):
            if number % 27 == 0:
                tostring += "|\n+---------+---------+---------+\n"
            elif number % 9 == 0:
                tostring += "|\n"
            if number % 3 == 0:
                tostring += "|"
            tostring += " " + str(self.layout[number]) + " "
        tostring += "|\n+---------+---------+---------+\n"
        return tostring

    def compare(self, sudoku):
        """"""
        diff = [] 
        for number in range(len(self.layout)):
            if self.layout[number] != sudoku.layout[number]:
                diff.append(self.layout[number])
        return diff
    
    def read_file(self, path:str):
        """"""
        layout = []
        with open(path, 'rt') as file:
            input = file.read()
        for c in input:
            if c != "|" and c != "\n" and c != "-":
                if int(c) > 0:
                    layout.append(c)
                else:
                    layout.append(int(c))
        return layout
    
    def get_fitness(self) -> int:
        """Evaluates a given sudoku configuration as an integer value."""
        fitness:int = 0
        # For each sub-structure contained in a sudoku board:
        for i in range(0,9):
            # And for each number a sub-structure should have:
            for number in self.INT_RANGE:
                if number not in self.column(i):
                    fitness += 1
                if number not in self.row(i):
                    fitness += 1
                if number not in self.grid(i):
                    fitness += 1
        return fitness