import queue
import copy
import search

class Problem(object):

    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, size, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal
        self.size = size
        self.nodeNum = 0

    def actions(self, state):
        if self.size == 4:
            return [val in range(1,5)]
        else:
            return [val in range(1,10)]

    def result(self, state, r, c, action):
        state[r][c] = action
        self.nodeNum = self.nodeNum+1
        return copy.deepcopy(state)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError
class Node:
    def __init__(self, r, c, state):
        self.r = r
        self.c = c
        self.state = state
        self.next = None
        self.childern = None
        self.parent = None

def sudoku_solver(table, search):
    sudoku = []
    c = 0
    if len(table) == 16:
        m = 4
    else:
        m = 9

    for i in range(m):
        sudoku.append([0] * m)
        for j in range(m):
            if table[c] == '.':
                sudoku[i][j] = 0
            else:
                sudoku[i][j] = int(table[c])
            c = c + 1
    board = search.Problem(sudoku,m)
    if search == "bfs":
        bfs(board)
    elif search == "dfs":
        dfs(sudoku, m)


#########################################################################################
def breadth_first_tree_search(problem):
    frontier = queue.Queue()
    gameSolved = False;
    (r,c) = next_empty_space(problem.inital,0,0)

    frontier.put([Node(r,c,problem.initial)])  # FIFO queue

    while frontier:
        node = frontier.get()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None


    #(r, c) = next_empty_space(puzzle, 0, 0)
    #(lastR, lastC) = lastBox(puzzle)

    #for k in range(1, max + 1):
       # puzzle[r][c] = k
       # curr = Node(False, r, c, copy.deepcopy(puzzle))
       # if playable(puzzle, r, c, k) is True:
           # waitList.put(curr)

    while not waitList.empty() and not gameSolved:
        curr = waitList.get()
        puzzle = curr.value
        (r, c) = next_empty_space(puzzle, curr.r, curr.c)
        if r == -1:
            gameSolved = True
        elif r == lastR and c == lastC:
            k = 1
            while not gameSolved and k < max + 1:
                puzzle[r][c] = k
                curr = Node(False, r, c, copy.deepcopy(puzzle))
                nodeNum = nodeNum + 1
                if playable(puzzle, r, c, k):
                    gameSolved = True
                    donePuzzle = puzzle
                else:
                    k = k + 1
        else:
            for k in range(1, max + 1):
                puzzle[r][c] = k
                curr = Node(False, r, c, copy.deepcopy(puzzle))
                nodeNum = nodeNum + 1
                if playable(curr.value, r, c, k):
                    waitList.put(curr)
    if gameSolved:
        for row in donePuzzle:
            print(row)
    else:
        print("error")


#########################################################################################
def dfs(puzzle, max):
    waitList = queue.Queue()
    gameSolved = False;
    (r, c) = next_empty_space(puzzle, 0, 0)
    (lastR, lastC) = lastBox(puzzle)
    k = 1
    playable = False
    while k <= max and not playable:
        playable = playable(puzzle, curr.r, curr.c, k)
        puzzle[r][c] = k
        curr = Node(False, r, c, copy.deepcopy(puzzle))
        k = k + 1


#########################################################################################


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
    sudoku_solver(line, algor)


if __name__ == "__main__": main()






