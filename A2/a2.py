# -*- coding: utf-8 -*-
import logic
from utils import expr
from planning import Action
import planning


greater = {}
def fol(equation):
   return 0
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
feedbackKB = logic.PropKB()
for s in "C==>(J); ~C==>(A); (M&(I|S)&C)==>T;(M&(I|S)&~C)==>D; ((N|(I&~M))&~C)==>E; ((I&C&~M)|(N&S&C))==>U; (N&S&~C)==>H; (~M&(S^N)&C)==>R".split(';'):
    feedbackKB.tell(expr(s))


def giveFeedback(studentState):
    expression = []
    if studentState.find("CorrectAnswer") == -1 or studentState.find("IncorrectAnswer") != -1:
        expression.append('~C')
        feedbackKB.tell(expr('~C'))
    else:
        expression.append('C')
        feedbackKB.tell(expr('C'))
    if studentState.find("NewSkill") == -1:
        expression.append("~N")
        feedbackKB.tell(expr("~N"))
    else:
        expression.append("N")
        feedbackKB.tell(expr("N"))
    if studentState.find("MasteredSkill") == -1:
        expression.append(expr("~M"))
        feedbackKB.tell("~M")
    else:
        expression.append(expr("M"))
        feedbackKB.tell("M")
    if studentState.find("CorrectStreak") == -1:
        expression.append("~S")
        feedbackKB.tell(expr("~S"))
    else:
        expression.append("S")
        feedbackKB.tell(expr("S"))
    if studentState.find("IncorrectStreak") != -1:
        expression.append("I")
        feedbackKB.tell(expr("I"))
    M = ['R','U','T','H', 'D', 'E', 'J','A']
    i = 0
    while i < 8 and not feedbackKB.ask_if_true(expr(M[i])):
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
    middle = equation.find('=')
    end = len(equation)
    num = ""
    Left = {}
    Right = {}
    Right['var'] =[]
    Right['con'] = []
    Left['var'] = []
    Left['con'] = []
    leftcount = 0
    rightcount = 0
    for i in range(end):
        if len(num) == 0 and equation[i] == '-':
            num = equation[i]
        elif equation[i].isdigit():
            num = num+equation[i]
        elif equation[i] == 'x':
            if i < middle or i == middle:
                side = 'Left'
            else:
                side = 'Right'
            if len(num) == 0:
                num = 1
            elif num == '-':
                num = -1
            if side == 'Right':
                Right['var'].append(int(num))
            else:
                Left['var'].append(int(num))
            num=''
        elif len(num) > 0 and not (equation[i].isdigit()):
            if i < middle or i == middle:
                side = 'Left'
            else:
                side = 'Right'
            if side == 'Right':
                Right['con'].append(int(num))
            else:
                Left['con'].append(int(num))
            num = ''
            if equation[i] == '-':
                num = '-'
    if len(num) > 0:
        Right['con'].append(int(num))
    toSolve =[]
    while len(Right['var']) > 0 or len(Right['con']) != 1 or len(Left['var']) != 1 or len(Left['con']) > 0:
        if len(Left['var']) > 1:
            num = 0
            end = len(Left['var'])
            for i in range(end):
                num = num + Left['var'].pop()
            Left['var'].append(num)
            if num < 0:
                greater[1] = False
            else:
                greater[1] = True
            toSolve.append('combine LHS variable terms’')
        elif len(Right['con']) > 1:
            num = 0
            end = len(Right['con'])
            for i in range(end):
                num = num + Right['con'].pop()
            Right['con'].append(num)
            toSolve.append('combine RHS constant terms’')
        elif len(Right['var']) > 0:
            num = Right['var'].pop()
            num = num * -1
            Left['var'].append(num)
            toSolve.append('add '+str(num)+'x')
        elif len(Left['con']) > 0:
            num = Left['con'].pop()
            print(num)
            num = num * -1
            Right['con'].append(num)
            toSolve.append('add ' + str(num))
    if Left['var'][0] != 1:
        num = Left['var'][0]
        Left['var'][0] = 1
        Right['con'][0] = Right['con'][0]/num
        toSolve.append('divide '+str(num))

    return toSolve

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
def get_num(numberString):
    num = ''
    start = False
    end = False
    i = 0
    while not end and i < len(numberString):
        if numberString[i].isdigit():
            start = True
            num = num + numberString[i]
        elif not numberString.isdigit() and start:
            end = True
        i = i + 1
    return str(num)

def predictSuccess(current_skills, equation):
    greater.clear()
    skills_knowledge = logic.FolKB(map(expr, ['Positive(x) & Variable(x) ==>Add(x, S1)', 'Negative(x) & Variable(x) ==>Add(x, S2)', 'Positive(x) & Constant(x) ==>Add(x, S3)', 'Negative(x) & Constant(x) ==>Add(x, S4)',
                                              'Positive(x)==>Divide(x, S5)', 'Negative(x)==>Divide(x, S6)', 'Constant(x) & Constant(y) ==>Combine(Constant, S9)',
                                              'Greater(x)==>Combine(Variable, S7)', 'Lesser(x)==>Combine(Variable, S8)']))
    #,

    actions_list = solveEquation(equation)
    if greater[1]:
        skills_knowledge.tell(expr('Greater(True)'))
    else:
        skills_knowledge.tell(expr('Lesser(True)'))
    skills_needed = []
    x = ''
    for action in actions_list:
        if action.find('add') != -1:
            num = get_num(action)
            if action.find('-') == -1:
                skills_knowledge.tell(expr('Positive('+num+')'))
            else:
                skills_knowledge.tell(expr('Negative('+num+')'))
            if action.find('x') == -1:
                skills_knowledge.tell(expr('Constant('+num+')'))
            else:
                skills_knowledge.tell(expr('Variable('+num+')'))
            x = skills_knowledge.ask(expr('Add('+num+', y)'))[expr('y')]

        elif action.find('divide') != -1:
            num = get_num(action)
            if action.find('-') == -1:
                skills_knowledge.tell(expr('Positive('+num+')'))
            else:
                skills_knowledge.tell(expr('Negative('+num+')'))
            x = skills_knowledge.ask(expr('Divide(' + num + ', y)'))[expr('y')]

        elif action.find('constant') != -1:
           x =  skills_knowledge.ask(expr('Combine(Constant, y)'))[expr('y')]

        elif action.find('variable') != -1:
            x = skills_knowledge.ask(expr('Combine(Variable, z)'))[expr('z')]
        skill = str(x)
        if current_skills.count(skill) == 0:
            skills_needed.append(skill)
    missing_skills = SAMPLE_MISSING_SKILLS
    return skills_needed


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
