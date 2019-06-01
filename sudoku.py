import cv2,time
import sys
from SudokuExtractor import extract_sudoku
from NumberExtractor import extract_number

def output(a):
    sys.stdout.write(str(a))

def display_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            cell = sudoku[i][j]
            if cell == 0 or isinstance(cell, set):
                output('0')
            else:
                output(cell)
            if (j + 1) % 3 == 0 and j < 8:
                output(' |')

            if j != 8:
                output('  ')
        output('\n')
        if (i + 1) % 3 == 0 and i < 8:
            output("--------+----------+---------\n")



def main(image_path):
    image = extract_sudoku(image_path)
    grid = extract_number(image) 
    global inputString
    inputString = grid.tolist()  
    


inputString =[]
startTime = time.time()
image_path = 'static/cache/sudoku.jpg'
main(image_path)
print(time.time()-startTime) 
