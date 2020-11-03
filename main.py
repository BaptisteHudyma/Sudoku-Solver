from sudokuLoader import *
from sudokuSolver import *

su = Sudoku_Loader("./examples/hard.png")
loadedGrid = su.get_sudoku_grid()
if loadedGrid is None:
    print("Could not load the sudoku grid")
    exit(1) 

sudoku = Sudoku()
sudoku.load(loadedGrid);

sudoku.display()

solutions = sudoku.solve ()
print("found", len(solutions), "solutions")
if len(solutions) > 0:
    sudoku.print_solution(solutions[0])

