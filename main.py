import sys
from sudoku import Sudoku
from evolutionary import Evolutionary

if __name__ == "__main__":
    print("Welcome to the Evolutionary Sudoku Solver.")
    while True:
        print("Please chose one of the following:")
        print("1 - Upload my Sudoku board as a.txt file.")
        print("2 - Enter my Sudoku board manually.")
        print("3 - Exit.")
        inp = int(input("\n"))
        if inp == 1:
            try:
                solver = Evolutionary(path=sys.argv[1])
            except:
                print("Error: The specified file/path does not exist. Please try again.")
        elif inp == 2:
            layout = []
            for number in sys.argv[1]:
                if number in Sudoku.INT_RANGE:
                    layout.append(int(number))
            if len(layout) < 81:
                print("Error: Not enough digits were retrieved from the inputted layout. Please try again.")
            solver = Evolutionary(sudoku=Sudoku(layout=layout))
        elif inp == 3:
            break
        else:
            print("Error: The input does not match any option. Please try again.")
        