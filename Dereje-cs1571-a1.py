import search
import csp


def sudokuSolver(line, algor):
    if algor == "backtracking":
        puzzle = csp.Sudoku(line)
        csp.backtracking_search(puzzle, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
        puzzle.display(puzzle.infer_assignment())
    else:
        if len(line) == 16:
            size = 4
        else:
            size = 9
        board = []
        c = 0
        for i in range(size):
            board.append([0] * size)
            for j in range(size):
                if line[c] == '.':
                    board[i][j] = 0
                else:
                    board[i][j] = int(line[c])
                c = c + 1

        if len(line) == 16:
            sudoku = search.Problem(board, [1, 2, 3, 4])
        else:
            sudoku = search.Problem(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        if algor == "bfs":
            pie = search.breadth_first_tree_search(sudoku)
        else:
            pie = search.depth_first_tree_search(sudoku)
        for row in pie.state:
            print(row)


def scheduleCourses(file, slots):
    index = 0
    f = open(file, 'r')
    classList = []
    for line in f.readlines():
        classList.append(Classes(line))
        classList[index].display()
        index = index + 1
class Sections:
    def __init__(self, teach):
        self.teach = teach
        self.section = 0
    def display(self):
        print("Professor {} sections {}".format(self.teach, self.section))

class Classes:
    def __init__(self,line):
        start = 0
        location = line.find(';', start)
        self.classNum = line[start:location]

        start = location + 1
        location = line.find(';', start)
        start = location +1
        self.classOffers = int(line[start])

        start = start + 6
        self.teachers = []
        location = line.find(';',start)

        teachNum = 0
        teachLoc = line.find(',',start,location)
        while teachLoc != -1:
            self.teachers.append(Sections(line[start:teachLoc]))
            start = teachLoc + 1
            teachLoc = line.find(',', start, location)
            teachNum = teachNum + 1

        self.teachers.append(Sections(line[start:location]))
        start = location + 1
        teachNum = teachNum + 1

        for i in range(teachNum):
            self.teachers[i].seaction = int(line[start])
            start = start+2
        end = len(line)
        self.areas = []
        if start < end:
            location = line.find(',', start)
            while location != -1:
                self.areas.append(line[start:location])
                start = location + 1
                location = line.find(',',start)
            lastLoc = line[start:end]
            if '\n' in lastLoc:
                lastLoc = lastLoc[:len(lastLoc)-1]
            self.areas.append(lastLoc)
    def display(self):
        print("Class Number {}, Offerings {}".format(self.classNum, self.classOffers))
        print(self.areas)
        for i in range(len(self.teachers)):
            print(self.teachers[i].display)