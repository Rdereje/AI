import probability4e

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

def q8():
    T, F = True, False
    network = probability4e.BayesNet([('Accurate', [], 0.90),
                          ('ProblemSize', [], 0.90),
                          ('ConversationLength', ['ProblemSize'],
                           {T: probability4e.ProbDist('X',{'short':.4, 'medium':.4,'long':.6}),
                            F:probability4e.ProbDist('X',{'short':.2, 'medium':.3,'long':.5})}),
                          ('Resolved', ['Accurate', 'ConversationLength'],
                           {(T,'short'):.3, (T,'medium'):.5, (T,'long'):.7,
                            (F,'short'):.2, (F,'medium'):.3, (F,'long'):.4})])

    probability4e.enumeration_ask('Resolved', dict(ConversationLength='long', ProblemSize=F, Accurate=T), network).show_approx()


