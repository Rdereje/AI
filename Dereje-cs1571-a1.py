import search
import re
import csp

def sudokuSolver(line, algor):
    puzzle = csp.Sudoku(line)
    puzzle.display(puzzle.infer_assignment())




def lastBox(table):
    size = len(table)
    r = size - 1
    c = size - 1
    while table[r][c] != 0:
        if c == 0:
            r = r - 1
            c = size - 1
        else:
            c = c - 1
    return (r, c)


def next_empty_space(table, r, c):
    size = len(table)
    i = r
    j = c
    found = False
    while table[i][j] != 0:
        j = j + 1
        if j == size:
            i = i + 1
            j = 0
    if table[i][j] == 0:
        return (i, j)
    return (-1, -1)


def playable(table, r, c, value):
    size = len(table)
    for i in range(size):
        if table[r][i] == value and i != c:
            return False
        if table[i][c] == value and i != r:
            return False
    if size == 4:
        div = 2
    else:
        div = 3
    blockr = (r // div) * div
    blockc = (c // div) * div
    for i in range(blockr, blockr + div):
        for j in range(blockc, blockc + div):
            if table[i][j] == value and (i != r and j != c):
                return False
    return True


def main():
    line = input("Input string")
    algor = input("Input seach algor")
    sudokuSolver(line, algor)


if __name__ == "__main__": main()
