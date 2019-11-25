# -*- coding: utf-8 -*-
import logic
from utils import expr
from planning import Action
import planning

greater = {}


def fol(equation):
    fol_list = []
    middle = equation.find('=')
    end = len(equation)
    symbol = 0
    ch = ['A', 'B', 'C', 'D']
    num = ""
    for i in range(end):
        if len(num) == 0 and equation[i] == '-':
            num = equation[i]
        elif equation[i].isdigit():
            num = num + equation[i]
        elif equation[i] == 'x':
            if i < middle:
                side = 'Left'
            else:
                side = 'Right'
            if len(num) == 0:
                num = '1'
            elif num == '-':
                num = '-1'
            if side == 'Right':
                fol_list.append('Right(Variable, ' + ch[symbol] + ')')
                fol_list.append('Value(' + ch[symbol] + ', ' + num + ')')
                symbol = symbol + 1
            else:
                fol_list.append('Left(Variable, ' + ch[symbol] + ')')
                fol_list.append('Value(' + ch[symbol] + ', ' + num + ')')
                symbol = symbol + 1
            num = ''
        elif len(num) > 0 and not (equation[i].isdigit()):
            if i < middle or i == middle:
                fol_list.append('Left(Constant, ' + ch[symbol] + ')')
                fol_list.append('Value(' + ch[symbol] + ', ' + num + ')')
                symbol = symbol + 1
            else:
                fol_list.append('Right(Constant, ' + ch[symbol] + ')')
                fol_list.append('Value(' + ch[symbol] + ', ' + num + ')')
                symbol = symbol + 1
            num = ''
            if equation[i] == '-':
                num = '-'
    if len(num) > 0:
        fol_list.append('Right(Constant, ' + ch[symbol] + ')')
        fol_list.append('Value(' + ch[symbol] + ', ' + num + ')')
        symbol = symbol + 1
    return fol_list


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
# 1 = R
# 2 = U
# 3 = T
# 4 = H
# 5 = D
# 6 = E
# 7 = J
# 8 = A
feedbackKB = logic.PropKB()
for s in "C==>(J); ~C==>(A); (M&(I|S)&C)==>T;(M&(I|S)&~C)==>D; ((N|(I&~M))&~C)==>E; ((I&C&~M)|(N&S&C))==>U; (N&S&~C)==>H; (~M&(S^N)&C)==>R".split(
        ';'):
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
    M = ['R', 'U', 'T', 'H', 'D', 'E', 'J', 'A']
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

def create_fol():
    solve = logic.FolKB()
    solve.tell(expr('Left(Variable, a) & Left(Variable, b) ==> Left(Variable, X)'))
    solve.tell(expr('Right(Constant, a) & Right(Constant, b) ==> Right(Constant, Y)'))
    solve.tell(expr('Left(Variable, a) & Left(Variable, b) & Same(a!=b)==> RightVariableCombine(a,b)'))
    solve.tell(expr('Right(Constant, a) & Right(Constant, b) ==> LeftVariableCombine(a,b)'))
    return solve


def combine(string, solve, term):
    term_A = str(solve.ask(expr(string+', x)'))[expr('x')])
    num_A = str(solve.ask(expr('Value(' + term_A + ', y)'))[expr('y')])
    solve.retract(expr(string+', ' + term_A + ')'))
    solve.retract(expr('Value(' + term_A + ', ' + num_A + ')'))

    term_B = str(solve.ask(expr(string+', x)'))[expr('x')])
    num_B = str(solve.ask(expr('Value(' + term_B + ', y)'))[expr('y')])
    solve.retract(expr(string+', ' + term_B + ')'))
    solve.retract(expr('Value(' + term_B + ', ' + num_B + ')'))

    new_num = int(num_A) + int(num_B)
    solve.tell(expr(string+', '+term+')'))
    solve.tell(expr('Value('+term+',' + str(new_num) + ')'))


def solveEquation(equation):
    greater.clear()
    toSolve = []
    fol_list = fol(equation)
    solve = logic.FolKB()
    for terms in fol_list:
        solve.tell(expr(terms))

    while solve.ask(expr('Right(Variable,x)')) is not False:
        term = str(solve.ask(expr('Right(Variable, x)'))[expr('x')])
        num = str(solve.ask(expr('Value('+term+', y)'))[expr('y')])
        solve.retract(expr('Right(Variable, '+term+')'))
        solve.retract(expr('Value('+term+', '+num+')'))

        new_num = str(int(num) * -1)
        solve.tell(expr('Left(Variable, '+term+')'))
        solve.tell(expr('Value(' + term + ', ' + new_num + ')'))
        toSolve.append('add '+new_num+'x')

    while solve.ask(expr('Left(Constant,x)')) is not False:
        term = str(solve.ask(expr('Left(Constant, x)'))[expr('x')])
        num = str(solve.ask(expr('Value(' + term + ', y)'))[expr('y')])
        solve.retract(expr('Left(Constant, ' + term + ')'))
        solve.retract(expr('Value(' + term + ', ' + num + ')'))

        new_num = str(int(num) * -1)
        solve.tell(expr('Right(Constant, ' + term + ')'))
        solve.tell(expr('Value(' + term + ', ' + new_num + ')'))
        toSolve.append('add ' + new_num)
    num =[]

    while solve.ask(expr('Left(Variable, s)')) is not False:
        t = str(solve.ask(expr('Left(Variable, s)'))[expr('s')])
        n = str(solve.ask(expr('Value(' + t + ', y)'))[expr('y')])
        solve.retract(expr('Left(Variable, ' + t + ')'))
        solve.retract(expr('Value(' + t + ', ' + n + ')'))
        num.append(n)
    while len(num) > 1:
        temp = num.pop(0)
        temp_t = num.pop(0)
        num.append(int(temp) + int(temp_t))
        toSolve.append('combine LHS variable terms’')
    greater['1'] = num[0]
    divide = num[0]
    num.clear()
    while solve.ask(expr('Right(Constant, s)')) is not False:
        t = str(solve.ask(expr('Right(Constant, s)'))[expr('s')])
        n = str(solve.ask(expr('Value(' + t + ', y)'))[expr('y')])
        solve.retract(expr('Right(Constant, ' + t + ')'))
        solve.retract(expr('Value(' + t + ', ' + n + ')'))
        num.append(n)
    while len(num) > 1:
        temp = num.pop(0)
        temp_t = num.pop(0)
        num.append(int(temp) + int(temp_t))
        toSolve.append('combine RHS constant terms’')
    solve.tell(expr('Right(Constant, Y)'))
    solve.tell(expr('Value(Y, ' + str(num[0]) + ')'))

    if divide != 1:
        toSolve.append('divide '+str(divide))

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


skills_knowledge = logic.FolKB(map(expr, ['Positive(x) & Variable(x) ==>Add(x, S1)',
                                          'Negative(x) & Variable(x) ==>Add(x, S2)',
                                          'Positive(x) & Constant(x) ==>Add(x, S3)',
                                          'Negative(x) & Constant(x) ==>Add(x, S4)',
                                          'Positive(x)==>Divide(x, S5)', 'Negative(x)==>Divide(x, S6)',
                                          'Constant(x) & Constant(y) ==>Combine(Constant, S9)',
                                          'Greater(x)==>Combine(Variable, S7)', 'Lesser(x)==>Combine(Variable, S8)']))


def predictSuccess(current_skills, equation):
    actions_list = solveEquation(equation)
    return skill_list(current_skills, actions_list)
    missing_skills = SAMPLE_MISSING_SKILLS


def skill_list(current_skills, actions_list):

    delete_later = []
    if greater['1'] > -1:
        skills_knowledge.tell(expr('Greater(True)'))
        delete_later.append(expr('Greater(True)'))
    else:
        skills_knowledge.tell(expr('Lesser(True)'))
        delete_later.append(expr('Lesser(True)'))
    skills_needed = []
    x = ''
    for action in actions_list:
        if action.find('add') != -1:
            num = get_num(action)
            if action.find('-') == -1:
                skills_knowledge.tell(expr('Positive(' + num + ')'))
                delete_later.append(expr('Positive(' + num + ')'))
            else:
                skills_knowledge.tell(expr('Negative(' + num + ')'))
                delete_later.append(expr('Negative(' + num + ')'))
            if action.find('x') == -1:
                skills_knowledge.tell(expr('Constant(' + num + ')'))
                delete_later.append(expr('Constant(' + num + ')'))
            else:
                skills_knowledge.tell(expr('Variable(' + num + ')'))
                delete_later.append(expr('Variable(' + num + ')'))
            x = skills_knowledge.ask(expr('Add(' + num + ', y)'))[expr('y')]

        elif action.find('divide') != -1:
            num = get_num(action)
            if action.find('-') == -1:
                skills_knowledge.tell(expr('Positive(' + num + ')'))
                skills_knowledge.tell(expr('Positive(' + num + ')'))
            else:
                skills_knowledge.tell(expr('Negative(' + num + ')'))
                skills_knowledge.tell(expr('Negative(' + num + ')'))
            x = skills_knowledge.ask(expr('Divide(' + num + ', y)'))[expr('y')]

        elif action.find('constant') != -1:
            x = skills_knowledge.ask(expr('Combine(Constant, y)'))[expr('y')]

        elif action.find('variable') != -1:
            x = skills_knowledge.ask(expr('Combine(Variable, z)'))[expr('z')]
        skill = str(x)
        if current_skills.count(skill) == 0:
            skills_needed.append(skill)
    for actions in delete_later:
        skills_knowledge.retract(actions)
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

actions_taken = []
streak = 0


def stepThroughProblem(equation, action, current_skills):
    global streak
    message = ''
    current_action_needed = len(actions_taken)

    actions_needed = solveEquation(equation)
    if streak >= 3:
        message = message + 'CorrectStreak'
    if streak <= -3:
        message = message + 'IncorrectStreak '
    if action == actions_needed[current_action_needed]:
        message = message + 'CorrectAnswer'
        if streak < 0:
            streak = 0
        streak = streak + 1
        actions_taken.append(action)
    else:
        if streak > 0:
            streak = 0
        streak = streak - 1
    skill = skill_list(current_skills, [action])
    if len(skill) > 0:
        message = message + 'NewSkill'
        current_skills.append(skill[0])
    else:
        message = message + 'MasteredSkill'

    updated_skills = current_skills
    if len(actions_taken) == actions_needed:
        actions_taken.clear()
        streak = 0
    return [giveFeedback(message), updated_skills]
