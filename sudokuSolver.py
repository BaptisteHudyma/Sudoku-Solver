from constraint import *

class Sudoku :
    def __init__(self):
        self.indexes = range(81)   #grid of 9*9
        self.grid = [0 for i in range(81)]

        self.solver = Problem()


    def display(self):
        self.print_solution(self.grid)

    def add_number(self, coordX, coordY, number):
        if not isinstance(number, int):
            print("Number must be an integer between 1 and 9")
            return
        if number < 1 or number > 9:
            print("Numbers must be between 1 and 9")
            return
        if coordX < 0 or coordX > 8:
            print("X coordinates must be between 0 and 8")
            return
        if coordY < 0 or coordY > 8:
            print("Y coordinates must be between 0 and 8")
            return
        self.grid[coordX * 9 + coordY] = number; 


    def solve(self):
        self.set_constraints()
        return self.solver.getSolutions()


    def load(self, sudokuGridNumbers):
        self.grid = [0 for i in range(81)]
        for i in range(81):
            try:
                self.grid[i] = sudokuGridNumbers[i];
            except IndexError:
                continue   #index do not exist
    

    def print_solution(self, solution):
        #display on solution as a sudoku grid
        temporaryGrid = [0 for i in range(81)]
        for i in range(81):
            try:
                temporaryGrid[i] = solution[i];
            except IndexError:
                continue

        displayStr = ""
        displayStr += "\n------------------------------\n"
        for i in range(0, 9):
            for j in range(0, 3):
                displayStr += str(temporaryGrid[i * 9 + 3 * j : i * 9 + 3 * (j+1) ] )
                displayStr += " | "
            if i%3 == 2:
                displayStr += "\n------------------------------\n"
            else:
                displayStr += "\n"
        print(displayStr)
        






#privates

    def set_constraints(self):
        #all numbers between 1 and 9
        for i in range(81):
            if self.grid[i] > 0:
                self.solver.addVariable(i, [self.grid[i]])
            else:
                self.solver.addVariable(i, range(1, 9+1))

        #sum of rows is 45
        for row in range(9):
            rowIndexes = [row * 9 + i for i in range(9)]
            self.solver.addConstraint(ExactSumConstraint(45),
                rowIndexes)
            self.solver.addConstraint(AllDifferentConstraint(),
                rowIndexes)

        #sum of columns is 45
        for col in range(9):
            colIndexes = [col + 9 * i for i in range(9)]
            self.solver.addConstraint(ExactSumConstraint(45),
                colIndexes)
            self.solver.addConstraint(AllDifferentConstraint(),
                colIndexes)

        #sum of subsquares is 45
        for i in range(3):
            for j in range(3):
                squareIndexes = self.get_square_indexes(i, j)
                self.solver.addConstraint(ExactSumConstraint(45),
                        squareIndexes)
                self.solver.addConstraint(AllDifferentConstraint(),
                        squareIndexes)
        


    def get_square_indexes(self, i, j):
        #return a list of the indexes inside the sudoku subsquare [i, j]
        #i and j in [0, 2]
        res = list()
        for m in range(3):
            res += self.indexes[i * 3 + j * 27 + m * 9 : 
                    i * 3 + j * 27 + m * 9 + 3]
        return res





                




