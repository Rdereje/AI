import probability

class Node:
    def __init__(self, type, probablity, level):
        self.type = type
        self.level = level
        self. probablity = probablity
def utility_not_frustrated(k):
    answer = 5*k
    answer = answer + -100
    return answer
def utility_frustrated(k):
    return 5*k
def maxValue(list, chance, index):
    if len(list) < index or len(list) == 0:
        list.append(chance)
    elif list[index].value < chance.value:
        list[index] = chance

def q2(turns):
    Presolved = 0.1
    Pnotresolved = 0.9
    Pfrustrated = 0.3
    Pnotfrustrated = 0.7
    d = 1
    respondUtility = 100
    list = []

    root = Node("Decision", 1, 1)
    list.append(root)
    respondValue = [None] * turns
    redirectValue = [None] * turns
    respondProbalilty = [None] * turns
    respondChanceNode = [None] * turns

    while(len(list)>0 and d <= turns):
        curr = list.pop()
        index = curr.level - 1
        if curr.type == "Decision":
            list.append(Node("Respond",curr.probablity, curr.level))
            list.append(Node("Redirect", curr.probablity, curr.level))
        elif curr.type == "Redirect":
            redirectValue[index] = curr.probablity * ((Pfrustrated * utility_frustrated(curr.level)) + Pnotfrustrated * utility_not_frustrated(curr.level))
        elif curr.type == "Respond":
            d = d+1
            respondValue[index] = Presolved * respondUtility * curr.probablity
            respondProbalilty[index] = curr.probablity
            list.append(Node("Decision",curr.probablity*Pnotresolved, curr.level+1))


    print(respondValue)
    print(redirectValue)
    i = len(respondValue) -1
    while i >= 0:
        if i == len(respondValue) -1:
            respondChanceNode[i] = respondValue[i]
        else:
            respondChanceNode[i] = respondChanceNode[i+1] + redirectValue[i+1] + respondValue[i]
        i = i -1

    print(respondChanceNode)

    i = 0
    path = ""
    redirect = False
    while i < turns and not redirect:
        if respondValue[i] > redirectValue[i]:
            path = path + ", Respond"
        else:
            path = path+", Redirect"
            redirect =True
        i = i + 1

    return path[2:]

def q3():
    return len(q2(30).split(', '))

def q8(A,B):
    T, F = True, False
    probability.BayesNet([('Accurate', '', 0.90),
                          ('ProblemSize', '', 0.90),
                          ('Long','ProblemSize',
                          {T:0.2, F:0.5}),
                          ('Resolved', 'Long Accurate',
                           {(T, T): 0.7, (T, F): 0.4, (F, T): .8, (F, F): 0.5}),
                          ('Frustrated', 'ProblemSize Long Accurate',
                           {(T,T,T):.6,(T,T,F):.8,(T,F,T):.5,(F,T,T):.7}
                           (F,T,F):)])

    burglary = BayesNet([('Burglary', '', 0.001),
                         ('Earthquake', '', 0.002),
                         ('Alarm', 'Burglary Earthquake',
                          {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
                         ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
                         ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})])







