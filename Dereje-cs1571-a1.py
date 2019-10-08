import search
import csp
import time


def sudokuSolver(line, algor):

    if algor == "backtracking":
        puzzle = csp.Sudoku(line)
        start = time.time()
        csp.backtracking_search(puzzle, select_unassigned_variable=csp.mrv,order_domain_values=csp.lcv, inference=csp.forward_checking)
        #csp.backtracking_search(puzzle, select_unassigned_variable=csp.lcvar, order_domain_values=csp.mcval, inference=csp.forward_checking)
        #csp.backtracking_search(puzzle,inference=csp.forward_checking)
        end = (time.time() - start)
        hope = str(puzzle.display(puzzle.infer_assignment()))
        f = open("sudoku.txt", "a+")
        f.write("solution for {} with {} is {}\n".format(line, algor, hope))
        f.write("completed in {} with {} nodes\n".format(end, puzzle.nassigns))
        f.write("")
        f.close()
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

        if algor == "bfs":
            if len(line) == 16:
                sudoku = search.Sudoku(board, [1, 2, 3, 4])
            else:
                sudoku = search.Sudoku(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
            start = time.time()
            pie, nodesCreated,maxNodes = search.breadth_first_tree_search(sudoku)
            end = (time.time() - start)
        else:
            if len(line) == 16:
                sudoku = search.Sudoku(board, [1, 2, 3, 4])
            else:
                sudoku = search.Sudoku(board, [9, 8, 7, 6, 5, 4, 3, 2, 1])
            start = time.time()
            pie, nodesCreated,maxNodes = search.depth_first_tree_search(sudoku)
            end = (time.time() - start)

        f = open("sudoku.txt", "a+")


        sol = ""
        n = len(pie.state)
        for i in range(n):
            for j in range(n):
                sol = sol+str(pie.state[i][j])
        f.write("solution for {} with {} is {}\n".format(line, algor,sol))
        f.write("With {} nodes created, with at most {} in memory, and {} to complete\n".format(nodesCreated,maxNodes,end))
        f.write("")
        f.close()


def scheduleCourses(file, slots):
    index = 0
    f = open(file, 'r')
    classList = []
    for line in f.readlines():
        offers = getClasses(line)
        for j in offers:
            classList.append(j)
    csp_list = csp.ClassProblem(classList,slots)
    csp_list.display()
    csp.backtracking_search(csp_list, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    csp_list.display()
        #classList[index].display()
        #index = index + 1

class Sections:
    def __init__(self, teach):
        self.teach = teach
        self.section = 0
    def display(self):
        print("Professor {} sections {}".format(self.teach, self.section))

class Classes:
    def __init__(self,classNum, teacher,section, area):
        self.classNum = classNum
        self.teacher = teacher
        self.section = section
        self.area = area




def getClasses(line):
    start = 0
    location = line.find(';', start)
    classNum = line[start:location]

    start = location + 1
    location = line.find(';', start)
    start = location +1
    classOffers = int(line[start])

    start = start + 6
    teachers = []
    location = line.find(';',start)

    teachNum = 0
    teachLoc = line.find(',',start,location)
    while teachLoc != -1:
        teachers.append(Sections(line[start:teachLoc]))
        start = teachLoc + 1
        teachLoc = line.find(',', start, location)
        teachNum = teachNum + 1

    teachers.append(Sections(line[start:location]))
    start = location + 1
    teachNum = teachNum + 1

    for i in range(teachNum):
        teachers[i].seaction = int(line[start])
        start = start+2
    end = len(line)
    areas = []
    if start < end:
        location = line.find(',', start)
        while location != -1:
            areas.append(line[start:location])
            start = location + 1
            location = line.find(',',start)
        lastLoc = line[start:end]
        if '\n' in lastLoc:
            lastLoc = lastLoc[:len(lastLoc)-1]
        areas.append(lastLoc)

    classlist = []
    for i in range(len(teachers)):
        for j in range(teachers[i].section):
            classlist.append(Classes(classNum,teachers[i].teach,j,areas))
    return classlist

def findPath(interOne, interTwo, aglor):
    return False
    

