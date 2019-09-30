import queue
import copy
class Node:
	def __init__(self, permanent, r, c,value):
		self.permanent = permanent
		self.r = r
		self.c = c
		self.value = value
		self.next = None
		self.childern = None
		self.parent = None
	def value(self):
		if self.permanent is False:
			self.value = self.value+1

def sudoku_solver(table, search):
	sudoku = []
	c = 0
	if len(table) == 16:
		m = 4
	else:
		m = 9
	
	for i in range(m):
		sudoku.append([0]*m)
		for j in range(m):
			if table[c] == '.':
				sudoku[i][j] = 0
			else:
				sudoku[i][j] = int(table[c])
			c = c+1

	if search == "bfs":
		bfs(sudoku, m)

#########################################################################################
def bfs(puzzle, size):
	waitList = queue.Queue()
	gameSolved = False;
	if size == 4:
		max = 4
	else:
		max = 9

	nodeNum = max
	(r,c) = next_empty_space(puzzle,0,0)
	(lastR,lastC) = lastBox(puzzle)

	for k in range(1,max+1):
		puzzle[r][c] = k
		curr = Node(False,r,c, copy.deepcopy(puzzle))
		if playable(puzzle, r, c, k) is True:
			waitList.put(curr)

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

def lastBox(table):
	size = len(table)
	r = size - 1
	c = size -1
	while table[r][c] != 0:
		if c == 0:
			r = r-1
			c = size -1
		else:
			c = c -1
	return (r,c)

def next_empty_space(table,r,c):
	size = len(table)
	i = r
	j = c
	found = False
	while table[i][j] != 0:
		j = j+1
		if j == size:
			i = i +1
			j = 0
	if table[i][j] == 0:
		return (i, j)
	return (-1,-1)

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
	blockr = (r//div)*div
	blockc = (c//div)*div
	for i in range(blockr, blockr + div):
		for j in range(blockc, blockc+div ):
			if table[i][j] == value and (i != r and j != c):
				return False
	return True



def main():
	line = input("Input string")
	algor = input("Input seach algor")
	sudoku_solver(line,algor)

if __name__ == "__main__": main()






		