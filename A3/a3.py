import probability4e

from collections import defaultdict, Counter
import itertools
import math
import random

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



class BayesNet(object):
    "Bayesian network: a graph of variables connected by parent links."

    def __init__(self):
        self.variables = []  # List of variables, in parent-first topological sort order
        self.lookup = {}  # Mapping of {variable_name: variable} pairs

    def add(self, name, parentnames, cpt):
        "Add a new Variable to the BayesNet. Parentnames must have been added previously."
        parents = [self.lookup[name] for name in parentnames]
        var = Variable(name, cpt, parents)
        self.variables.append(var)
        self.lookup[name] = var
        return self


class Variable(object):
    "A discrete random variable; conditional on zero or more parent Variables."

    def __init__(self, name, cpt, parents=()):
        "A variable has a name, list of parent variables, and a Conditional Probability Table."
        self.__name__ = name
        self.parents = parents
        self.cpt = CPTable(cpt, parents)
        self.domain = set(itertools.chain(*self.cpt.values()))  # All the outcomes in the CPT

    def __repr__(self): return self.__name__


class Factor(dict): "An {outcome: frequency} mapping."


class ProbDist(Factor):
    """A Probability Distribution is an {outcome: probability} mapping.
    The values are normalized to sum to 1.
    ProbDist(0.75) is an abbreviation for ProbDist({T: 0.75, F: 0.25})."""

    def __init__(self, mapping=(), **kwargs):
        if isinstance(mapping, float):
            mapping = {T: mapping, F: 1 - mapping}
        self.update(mapping, **kwargs)
        normalize(self)


class Evidence(dict):
    "A {variable: value} mapping, describing what we know for sure."


class CPTable(dict):
    "A mapping of {row: ProbDist, ...} where each row is a tuple of values of the parent variables."

    def __init__(self, mapping, parents=()):
        """Provides two shortcuts for writing a Conditional Probability Table.
        With no parents, CPTable(dist) means CPTable({(): dist}).
        With one parent, CPTable({val: dist,...}) means CPTable({(val,): dist,...})."""
        if len(parents) == 0 and not (isinstance(mapping, dict) and set(mapping.keys()) == {()}):
            mapping = {(): mapping}
        for (row, dist) in mapping.items():
            if len(parents) == 1 and not isinstance(row, tuple):
                row = (row,)
            self[row] = ProbDist(dist)


class Bool(int):
    "Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'"
    __str__ = __repr__ = lambda self: 'T' if self else 'F'


T = Bool(True)
F = Bool(False)


def P(var, evidence={}):
    "The probability distribution for P(variable | evidence), when all parent variables are known (in evidence)."
    row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row]


def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist


def sample(probdist):
    "Randomly sample an outcome from a probability distribution."
    r = random.random()  # r is a random point in the probability distribution
    c = 0.0  # c is the cumulative probability of outcomes seen so far
    for outcome in probdist:
        c += probdist[outcome]
        if r <= c:
            return outcome


def globalize(mapping):
    "Given a {name: value} mapping, export all the names to the `globals()` namespace."
    globals().update(mapping)
def joint_distribution(net):
    "Given a Bayes net, create the joint distribution over all variables."
    return ProbDist({row: prod(P_xi_given_parents(var, row, net)
                               for var in net.variables)
                     for row in all_rows(net)})

def all_rows(net): return itertools.product(*[var.domain for var in net.variables])

def P_xi_given_parents(var, row, net):
    "The probability that var = xi, given the values in this row."
    dist = P(var, Evidence(zip(net.variables, row)))
    xi = row[net.variables.index(var)]
    return dist[xi]

def prod(numbers):
    "The product of numbers: prod([2, 3, 5]) == 30. Analogous to `sum([2, 3, 5]) == 10`."
    result = 1
    for x in numbers:
        result *= x
    return result

def enumeration_ask(X, evidence, net):
    "The probability distribution for query variable X in a belief net, given evidence."
    i    = net.variables.index(X) # The index of the query variable X in the row
    dist = defaultdict(float)     # The resulting probability distribution over X
    for (row, p) in joint_distribution(net).items():
        if matches_evidence(row, evidence, net):
            dist[row[i]] += p
    return ProbDist(dist)

def matches_evidence(row, evidence, net):
    "Does the tuple of values for this row agree with the evidence?"
    return all(evidence[v] == row[net.variables.index(v)]
               for v in evidence)

def q8(A,B):
    T, F = True, False
    network = BayesNet()
    network.add('Accurate', [], 0.90)
    network.add('ProblemSize', [], 0.90)
    network.add('ConversationLength', ['ProblemSize'],
                {T: ProbDist(short=.4, medium=.4,long=.6),
                 F: ProbDist(short=.2, medium=.3,long=.5)})
    network.add('Resolved', ['Accurate', 'ConversationLength'],
                    {(T,'short'):.3, (T,'medium'):.5, (T,'long'):.7,
                     (F,'short'):.2, (F,'medium'):.3, (F,'long'):.4})
    network.add('Frustrated', ['ProblemSize', 'ConversationLength', 'Accurate'],
                {(T,'short',T):.2,(T,'short',F):.4,(T,'medium',T):.3,(T,'medium',F):.5, (T,'long',T):.6,(T,'long',F):.8,
                 (F,'short',T):.3,(F,'short',F):.5,(F,'medium',T):.6,(F,'medium',F):.8, (F,'long',T):.7,(F,'long',F):.9})
    globalize(network.lookup)
    if A == 'Resolved':
        X = Resolved
    elif A=='Problem_Size':
        X = ProblemSize
    elif A == 'Conversation_Length':
        X = ConversationLength
    elif A == 'Accuracte':
        X = Accurate
    elif A == 'Frustrated':
        X = Frustrated

    variables = B.split(', ')
    Y = {}
    for v in variables:
        temp = v.split(':')
        if temp[0] == 'Resolved':
            left = Resolved
        elif temp[0] == 'Problem_Size':
            left = ProblemSize
        elif temp[0] == 'Conversation_Length':
            left = ConversationLength
        elif temp[0] == 'Accurate':
            left = Accurate
        elif temp[0] == 'Frustrated':
            left = Frustrated
        if temp[1] == 'T':
            right = T
        elif temp[1] == 'F':
            right = F
        else:
            right = temp[1]
        Y[left] = right

    print(enumeration_ask(X, Y, network))
    #{ConversationLength:'long', ProblemSize:F, Accurate:T}
