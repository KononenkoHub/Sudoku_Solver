import sys
import os
from copy import deepcopy
import sudoku


def output(a):
    sys.stdout.write(str(a))

   
field = sudoku.inputString

N = 9


def print_board(field):
    if not field:
        output('No solution')

        return
    for i in range(len(field)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(field[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(field[i][j])
            else:
                print(str(field[i][j]) + " ", end="")

def read(field):
    """ Read field into state (replace 0 with set of possible values) """

    state = deepcopy(field)
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if cell == 0:
                state[i][j] = set(range(1,10))

    return state

def fileup(field):
    f = open("static/out.html", "w")
    if not field:
        f.write('<h1 style="text-align:center; margin-top:180px; color:gray;">No solution. Load other picture...<h1>')
    else:
        f.write(
            '<table border="1"  bordercolor="#484848" width="350px" height="350px" style="text-align:center; font-size:25px;" bgcolor="#E8E8E8" > <tr>')
        for item in range(len(solve(state))):
            if item % 1 == 0 and item != 0:
                f.write("</tr> <tr>")
            for i in solve(state)[item]:
                f.write('<td>' + str(i) + '</td>')

        f.write('</tr> </table>')


state = read(field)


def done(state):

    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True


def propagate_step(state):

    new_units = False

    # propagate row rule
    for i in range(N):
        row = state[i]
        values = set([x for x in row if not isinstance(x, set)])
        for j in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    # propagate column rule
    for j in range(N):
        column = [state[x][j] for x in range(N)]
        values = set([x for x in column if not isinstance(x, set)])
        for i in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    # propagate cell rule
    for x in range(3):
        for y in range(3):
            values = set()
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    cell = state[i][j]
                    if not isinstance(cell, set):
                        values.add(cell)
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    if isinstance(state[i][j], set):
                        state[i][j] -= values
                        if len(state[i][j]) == 1:
                            val = state[i][j].pop()
                            state[i][j] = val
                            values.add(val)
                            new_units = True
                        elif len(state[i][j]) == 0:
                            return False, None

    return True, new_units

def propagate(state):

    while True:
        solvable, new_unit = propagate_step(state)
        if not solvable:
            return False
        if not new_unit:
            return True


def solve(state):


    solvable = propagate(state)

    if not solvable:
        return None

    if done(state):

        return state

    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if isinstance(cell, set):
                for value in cell:
                    new_state = deepcopy(state)
                    new_state[i][j] = value
                    solved = solve(new_state)
                    if solved is not None:
                        return solved
                return None





if __name__ == "__main__":
    print_board(solve(state))
    fileup(solve(state))





