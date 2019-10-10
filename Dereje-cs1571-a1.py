import search
import csp
import time
#my code class_constraints, ClassProblem(CSP),  degree(assignment, csp), lcvar(assignment,csp), mcval(var, assignment, csp): are in csp.py file
#class Node_Sudoku: and class Sudoku(Problem): is in search.py

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


class Classes:
    def __init__(self,classNum, teacher,section, area):
        self.classNum = classNum
        self.teacher = teacher
        self.section = section
        self.area = area

def scheduleCourses(file, slots):
    f = open(file, 'r')
    classList = []

    for line in f.readlines():
        offers = getClasses(line)
        for j in offers:
            classList.append(j)

    f.close()
    csp_list = csp.ClassProblem(classList,slots)
    csp.backtracking_search(csp_list, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, arc=csp.degree,inference=csp.mac)
    csp_list.display(csp_list.infer_assignment())


def getClasses(line):
    line = line.replace(" ", "")
    start = 0
    location = line.find(';')
    classNum = line[start:location]

    start = location + 1
    location = line.find(';', start)
    start = location +1
    classOffers = int(line[start])

    start = start + 6
    teachers = []
    sections = []
    location = line.find(';',start)

    teachNum = 0
    teachLoc = line.find(',',start,location)
    while teachLoc != -1:
        teachers.append(line[start:teachLoc])
        start = teachLoc + 1
        teachLoc = line.find(',', start, location)
        teachNum = teachNum + 1

    teachers.append(line[start:location])
    start = location + 1
    teachNum = teachNum + 1

    for i in range(teachNum):
        sections.append(int(line[start]))
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

    classSec = []
    for i in range(len(teachers)):
        for j in range(sections[i]):
            classSec.append(Classes(classNum,teachers[i],j,areas))
    return classSec

def findPath(interOne, interTwo, aglor):
    distance_list = []
    elevation_dict = {}
    distance_file = open("partC-distances.txt", 'r')
    for line in distance_file.readlines():
        inter1,inter2,distance = getDisInfo(line)
        distance_list.append(distanceEdge(inter1,inter2,distance))
    distance_file.close()
    location_file = open("partC-intersections.txt", 'r')
    for line in location_file.readlines():
        key,value = elevation(line)
        elevation_dict[key] = int(value)
    location_file.close()
    path_problem = getPath(interOne,interTwo,distance_list,elevation_dict)
    goal_node = search.astar_search(path_problem)
    print(goal_node.path_cost)
    path = goal_node.path()
    f = open("Navigating Around Campus.txt", "w+")
    for street in path:
        f.write("{},".format(street.state))
        print(street.state, end = ",")
    f.write("{}\n".format(goal_node.path_cost*10))
    f.close()
    print(goal_node.path_cost*10)

def getDisInfo(line):
    start = 0
    middle = line.find(',',start)
    end = line.find(',',middle+1)
    inter1 = line[start:end]
    start = end+1
    middle = line.find(',',start)
    end = line.find(',',middle+1)
    inter2 = line[start:end]
    start = end+1
    string_dis = line[start:]
    if '\n' in string_dis:
        string_dis = string_dis[:len(string_dis) - 1]
    float_dis = float(string_dis)
    return inter1,inter2,float_dis
def elevation(line):
    start = 0
    middle = line.find(',')
    end = line.find(',',middle+1)
    key = line[start:end]
    start = end+1
    end = line.find(',',start)
    start = end+1
    end = line.find(',',start)
    start = end+1
    elevation = line[start:]
    if '\n' in elevation:
        elevation = elevation[:len(elevation) - 1]
    return key,elevation
class distanceEdge():
    def __init__(self,inter1,inter2,distance):
        self.inter1 = inter1
        self.inter2 = inter2
        self.distance = distance
    def display(self):
        print("{} - {} - {}".format(self.inter1,self.inter2,self.distance))
    def connectionsInfo(self, intersection):
        if self.inter1 == intersection:
            return self.inter2, self.distance
        if self.inter2 == intersection:
            return self.inter1, self.distance
    def isConnected(self,intersection):
        if self.inter1 == intersection or self.inter2 == intersection:
            return True
        return False
class getPath(search.Problem):

    def __init__(self,initial,goal,distance_list,elevation_dict):
        self.initial = initial
        self.goal = goal
        self.distance_list = distance_list
        self.elevation_dict = elevation_dict

        search.Problem.__init__(self, initial, goal)

    def actions(self, state):
        connected_location = []
        for edges in self.distance_list:
            if edges.isConnected(state):
                connected_location.append(edges)
        return connected_location

    def result(self,state,action):
        next_state,distance = action.connectionsInfo(state)
        return next_state
    def goal_test(self, state):
        return state == self.goal
    def path_cost(self,c, state1,action,state2):
        next_state , distance = action.connectionsInfo(state1)
        return c + distance
    def h(self, node):
        """ Return the heuristic value for a given state."""
        current_elevation = self.elevation_dict[node.state]
        goal_elevation = self.elevation_dict[self.goal]
        difference = (goal_elevation - current_elevation)/100 #if current intersection is going downhill than decrease distance

        return difference

    

