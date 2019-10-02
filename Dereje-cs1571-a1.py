import search
import csp
def sudokuSolver(line,algor):
    puzzle = csp.Sudoku(line)
    puzzle.display(puzzle.infer_assignment())

    if search != "backtracking":
        if len(line) == 16:
            size = 4
        else:
            size = 9
    board = []
    c = 0
    for i in range(size):
        board.append([0]*size)
        for j in range(size):
            if line[c] == '.':
                board[i][j] = 0
            else:
                board[i][j] = int(line[c])
            c = c+1

    if len(line) == 16:
        sudoku = search.Problem(board,[1,2,3,4])
    else:
        sudoku = search.Problem(board,[1, 2, 3, 4, 5, 6, 7, 8, 9])
    if algor == "bfs":
        pie = search.breadth_first_tree_search(sudoku)
    else:
        pie = search.depth_first_tree_search(sudoku)
    for row in pie.state:
        print(row)



def main():
    line = input("input string")
    algor = input("input search")
    sudokuSolver(line,algor)
