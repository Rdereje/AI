# -*- coding: utf-8 -*-
import logic
from utils import expr
from planning import Action
import planning

""" A2 Part A

    giveFeedback is a function that reads in a student state and returns a feedback message using propositional logic and proof by resolution. The rules
    for how to decide which message to return are given in the assignment description.
    
    studentState:   a String representing a conjunction of five possible symbols: CorrectAnswer, NewSkill, MasteredSkill, CorrectStreak, IncorrectStreak
                    For example, you could call giveFeedback('CorrectAnswer') or giveFeedback('MasteredSkill & CorrectStreak')
    
    feedbackMessage:a String representing one of eight feedback messages (M1 through M8 below). 
    
    Feel free to refactor the code to move M1 through M8 into a class, but the function call and return values should remain as specified below for our grading.
"""

M1 = 'Correct. Keep up the good work!'
M2 = 'Correct. I think you’re getting it!'
M3 = 'Correct. After this problem we can switch to a new problem.'
M4 = 'Incorrect. Keep trying and I’m sure you’ll get it!'
M5 = 'Incorrect. After this problem, we can switch to a new activity.'
M6 = 'Incorrect. The following is the correct answer to the problem.'
M7 = 'Correct.'
M8 = 'Incorrect.'
#1 = R
#2 = U
#3 = T
#4 = H
#5 = D
#6 = E
#7 = J
#8 = A
feedbackKB = logic.PropDefiniteKB()
for s in "C==>J; Z==>A;(M & I)==>B; (M & S)==>B; (N&I&Z)==>E; (N&S)==>N;(I&C)==>N; (N&C)==>U;(N&Z)==>H;(B&C)==>T; (B&Z)==>D;(N&C)==>R; (S&C)==>R".split(';'):
    feedbackKB.tell(expr(s))


def giveFeedback(studentState):
    expression = []
    if studentState.find("CorrectAnswer") == -1:
        expression.append('Z')
        feedbackKB.tell(expr('Z'))
    else:
        expression.append('C')
        feedbackKB.tell(expr('C'))
    if studentState.find("NewSkill") != -1:
        expression.append("N")
        feedbackKB.tell(expr("N"))
    if studentState.find("MasteredSkill") != -1:
        expression.append(expr("M"))
        feedbackKB.tell("M")
    if studentState.find("CorrectStreak") != -1:
        expression.append("S")
        feedbackKB.tell(expr("S"))
    if studentState.find("IncorrectStreak") != -1:
        expression.append("I")
        feedbackKB.tell(expr("I"))
    M = ['R','U','T','H', 'D', 'E', 'J','A']
    i = 0
    while (i < 8 and not logic.pl_fc_entails(feedbackKB, expr(M[i]))):
        i = i + 1
    for c in expression:
        feedbackKB.retract(expr(c))
    if i is 0:
        return M1
    elif i is 1:
        return M2
    elif i is 2:
        return M3
    elif i is 3:
        return M4
    elif i is 4:
        return M5
    elif i is 5:
        return M6
    elif i is 6:
        return M7
    elif i is 7:
        return M8
    else:
        return "error"


""" A2 Part B

    solveEquation is a function that converts a string representation of an equation to a first-order logic representation, and then
    uses a forward planning algorithm to solve the equation. 
    
    equation:   a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')
    
    plan:   return a list of Strings, where each String is a step in the plan. The Strings should reference the core actions described in the
            Task Domain part of the assignment description.
    
"""
SAMPLE_EQUATION = '3x-2=6'
SAMPLE_ACTION_PLAN = ['add 2', 'combine RHS constant terms', 'divide 3']


def solveEquation(equation):
    #PlanningProblem(initial='On(A, Table) & On(B, Table) & On(C, A) & Clear(B) & Clear(C)',
     #               goals='On(A, B) & On(B, C)',
      #              actions=[Action('Move(b, x, y)',
       #                             precond='On(b, x) & Clear(b) & Clear(y)',
        #                            effect='On(b, y) & Clear(x) & ~On(b, x) & ~Clear(y)',
         #                           domain='Block(b) & Block(y)'),
          #                   Action('MoveToTable(b, x)',
           #                         precond='On(b, x) & Clear(b)',
            #                        effect='On(b, Table) & Clear(x) & ~On(b, x)',
             #                       domain='Block(b) & Block(x)')],
              #      domain='Block(A) & Block(B) & Block(C)')

    initial = ''
    middle = equation.find('=')
    end = len(equation)
    num = ""
    leftcount = 0
    rightcount = 0
    domain=''
    for i in range(end):
        if len(num) == 0 and equation[i] == '-':
            num = equation[i]
        elif equation[i].isdigit():
            num = num+equation[i]
        elif equation[i] == 'x':
            if i < middle or i == middle:
                side = 'Left'
                if leftcount == 0:
                    var = 'A'
                    leftcount = leftcount + 1
                else:
                    var = 'B'
            else:
                side = 'Right'
                if rightcount == 0:
                    var = 'C'
                    rightcount = rightcount + 1
                else:
                    var = 'D'
            if len(num) == 0:
                num = '1'
                initial = initial + ' & isOne('+num+')'
            if side == 'Right':
                otherSide = 'Left'
            else:
                otherSide = 'Right'
            initial = initial + ' & Contains('+side+',  '+num+') & Variable('+num+')'
            domain = domain + " & Variable("+num+")"
            num=''
        elif len(num) > 0 and not (equation[i].isdigit()):
            if i < middle or i == middle:
                side = 'Left'
                if leftcount == 0:
                    var = 'A'
                    leftcount = leftcount + 1
                else:
                    var = 'B'
            else:
                side = 'Right'
                if rightcount == 0:
                    var = 'C'
                    rightcount = rightcount + 1
                else:
                    var = 'D'
            if side == 'Right':
                otherSide = 'Left'
            else:
                otherSide = 'Right'
            initial = initial +' & Contains('+side+', '+num+') & Constant(' + num + ')'
            domain = domain + ' & Constant('+num+')'
            num = ''
            if equation[i] == '-':
                num = '-'
    if len(num) > 0:
        if rightcount == 0:
            var = 'C'
        else:
            var = 'D'
        initial = initial + ' & Contains(Right, '+num+') & Constant(' + num + ')'
        domain = domain + ' & Constant('+num+')'
    initial = initial[3:]
    domain = domain[3:]
    initial = initial + ' & Contains(Y, Left)'
    goals = 'Contains(X, Right) & isOne(X) & Variable(X) & Contains(Right, Y) & Constant(Y)'
    goals='Contains(Right, Y) & Constant(Y)'
    #domain = 'Term(A) & Term(B) & Term(C) & Term(D) & Term(X) & Term(Y)'
    actions=[Action('AddRight(a)',
                    precond='Contains(Left, a) & Constant(a)',
                    effect='Contains(Right, a) & ~Contains(Left, a)'),
             Action('AddLeft(a)',
                    precond='Contains(Right, a) & Variable(a)',
                    effect='Contains(Left, a) & ~Contains(Right, a)'),
             Action('CombineLeft(a,b)',
                    precond='Contains(Left, a) & Contains(Left, b) & Variable(a) & Variable(b)',
                    effect='Contains(Left, a + b) & Contains(Left, X) & ~Contains(Left, a) & ~Contains(Left, b) & ~Variable(a) & ~Variable(b)'),
             Action('CombineRight(a, b)',
                    precond='Contains(Right, a) & Contains(Right, b) & Constant(a) & Constant(b)',
                    effect='Contains(Right, a+b), ~Contains(Right, b) & ~Contains(Right, a) & ~Constant(a) & ~Constant(b) & Contains(Right, Y) & Constant(Y)')]
    planningEquation = planning.PlanningProblem(initial=initial, goals=goals,actions=actions)

    plan = initial
    print(plan)
    print(domain)
    return planningEquation
 #              actions=[Action('Move(b, x, y)',
       #                             precond='On(b, x) & Clear(b) & Clear(y)',
        #                            effect='On(b, y) & Clear(x) & ~On(b, x) & ~Clear(y)',
         #                           domain='Block(b) & Block(y)'),
          #                   Action('MoveToTable(b, x)',
           #                         precond='On(b, x) & Clear(b)',
            #                        effect='On(b, Table) & Clear(x) & ~On(b, x)',
             #                       domain='Block(b) & Block(x)')],

""" A2 Part C

    predictSuccess is a function that takes in a list of skills students have and an equation to be solved, and returns the skills
    students need but do not currently have in order to solve the skill. For example, if students are solving the problem 3x+2=8, and have S7 and S8, 
    they would still need S4 and S5 to solve the problem.
    
    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)
    
    equation:   a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')
    
    missing_skills: A list of skills students need to solve the problem, represented by S1 through S9.
    
"""
CURRENT_SKILLS = ['S8', 'S9']
EQUATION = '3x+2=8'
SAMPLE_MISSING_SKILLS = ['S4', 'S5']


def predictSuccess(current_skills, equation):
    missing_skills = SAMPLE_MISSING_SKILLS
    return missing_skills


""" A2 Part D

    stepThroughProblem is a function that takes a problem, a student action, and a list of current student skills, and returns
    a list containing a feedback message to the student and their updated list of skills.
    
    equation: a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
    
    action: an action in the task domain. For example: 'add 2', 'combine RHS constant terms', 'divide 3'
    
    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)
    
    feedback_message: A feedback message chosen correctly from M1-M9.
    
    updated_skills: A list of skills students have after executing the action.
    
"""
CURRENT_SKILLS = ['S8', 'S9']
EQUATION = '3x+2=8'
ACTION = 'add -2'
UPDATED_SKILLS = ['S8', 'S9', 'S4']


def stepThroughProblem(equation, action, current_skills):
    feedback_message = M1
    updated_skills = UPDATED_SKILLS
    return [feedback_message, updated_skills]
