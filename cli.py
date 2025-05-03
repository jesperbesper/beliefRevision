from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr
from classes import belief_base, belief
#from sortedcontainers import SortedList

PROMT = '>>>'

def preprocess_logic_expr(expr_str):
    # Replace bi-implication `<->` with `Equivalent()`
    expr_str = expr_str.replace('<->', ',')  # Replace with argument comma
    if ',' in expr_str:
        expr_str = f'Equivalent({expr_str})'
    return expr_str

def parse_and_cnf(expr_str, neg=False):
    preprocessed = preprocess_logic_expr(expr_str)
    expr = parse_expr(preprocessed)
    if neg:
        return to_cnf(Not(expr), simplify=True)
    return to_cnf(expr, simplify=True)

def printHelper():
    print(f"""r: Revise belief
c: Clear BB
v: View BB
h: Help
q: Quit""")
    
def extractClauses(formula, clauses=None):
    if clauses is None:
        clauses = []

    if isinstance(formula, And):
        for arg in formula.args:
            extractClauses(arg, clauses)
    elif isinstance(formula, Or):
        clauses.append(list(formula.args))
    elif isinstance(formula, (Symbol, Not)):
        clauses.append([formula])
    else:
        raise ValueError(f"Unrecognized expression type: {formula}")

    return clauses

def revision():
    print('\nEnter a belief (Valid symbols: ~, &, |, >>, <->)')
    inp_str = input(PROMT)
    form = parse_and_cnf(inp_str)
    negForm = parse_and_cnf(inp_str, neg=True)
    try:
        clauses = extractClauses(form)
        negClauses = extractClauses(negForm)
        print(clauses)
        print(negClauses)
        b = belief(clauses)
        notB = belief(negClauses)
        #check if belif is entailed in BB by cnf res on negated
        if BB.entails(notB):
            print("Belief already in BB")
            return
        #check for contradiction by seeing if negated belief is entailed
        elif BB.entails(b):
            print("Belief contradicts BB")
            #todo: handle contradiction
            BB.add_belief(b)
            print("Belief added to BB")
            return
        else:
            print("Belief added to BB")
            BB.add_belief(b)
            return        
    except Exception as e:
        print(f'Invalid input: {e}')
        revision()
        return
    


def get_input():
    print("Belief-revision-engion:")
    printHelper()
    while True:
        print()    
        print('Enter action:')
        inp = input(PROMT)
        if  inp == 'h':
            printHelper()
        elif inp == 'q':
            quit()
        elif inp == 'c':
            BB.clear()
            print("BB cleared")
        elif inp == 'v':
            BB.print()
        elif inp == 'r':
            #handle revison
            revision()
        else:
            print("Please enter valid input:")



if __name__ == '__main__':
    #create BB
    BB = belief_base()
    get_input()
