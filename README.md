# Sudoku-Solver

This program can anayze an image of a sudoku using openCV an basic image filtering, extract the number using Tesseract OCR application, and use a constraint programming approch to solve every possibilities of the retrieved sudoku very efficiently.

## Solving technic
I decided to use a constraint approch instead of a classical one.

Constraint programming uses the properties of the solutions to find the solutions themselves instead of solving them using a classical method.
This methode can be easily used to solve this kind of restricted problems with amazing performances, but the computational cost augments drastictly when the number of solutions increases.
However, solving the puzzle will be extremly fast if the number of solutions is small.

Here, I implemened the classical sudoku constraint mathematically as 7 laws:
- A cell can only contain number between 1 and 9, whith 0 representing an unknown state
- The sum of a column is 45 (1 + 2 + ... + 9)
- The sum of a line is 45
- The sum of each subsquares is 45
- Each line, column and subsquare can contain each number from 1 to 9 only once

For fun, I'll try (someday) to implement other solving methods and compare them.

## Sudoku extraction
The extraction of the sudoku from an image is done by basic image transformations mainly borrowed from https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/, whith a few modifications to improve grid and number cleaning.

To detect the numbers in the cleaned sudoku grid, I used Tesseract OCR engine.
Tesseract is one of the greates open source OCR engine available.
Here I use it only for single numbers recognition, which is a bit like using a plane to visit a next door neightboor.
Hence it can induce problems because of it's capacity to detect some patterns (letters, multiple digits numbers, ...) instead of the targeted simple numbers.

I plan on training (more likely shamelessly stealing) a dedicated simple neural network, which will be faster and will hopfully present most edge cases.
Another improvement could be to use warp transformations to unskew the sudoku grid.


## Install & Use
Use `pip install -r requirements` to install necessary packages.

I used python 3.8.5 but any 3.5+ should work

Take a picture of a solved/partially solved sudoku or download one online, modify the path in main.py accordingly and let it roll.
