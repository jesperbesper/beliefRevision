<<<<<<< HEAD
from itertools import combinations

=======
from cli import parse_and_cnf, extractClauses
>>>>>>> ec3315028872dde92944e8e2931ba703d81b335b
class belief:
    def __init__(self, b, prio=0):
        self.b = b
        self.prio = prio

    def __eq__(self, other):
        return self.b == other.b
    
    def __str__(self):
        return str(self.b) 
    
    def __repr__(self):
        return f"belief({repr(self.b)})" 
    
    def setPrio(self, prio):
        if not isinstance(prio, int) and prio < 0 and prio >= 10:
            raise TypeError("Priority must be an integer between 0 and 10")
        self.prio = prio
        return
    
class belief_base:
    def __init__(self):
        self.beliefs = list()
    
    def clear(self):
        self.beliefs = list()


    def del_formula(self, form):
        for b in self.beliefs:
            if b == form:
                self.beliefs.remove(b)
                return
        return
    
    def add_belief(self, form):
        if not isinstance(form, belief):
            raise TypeError("Expected a belief instance")
        
        self.beliefs.append(form)
        return
    
    def print(self):
        print("Belief Base:")
        for b in self.beliefs:
            print(b)
        return
    
    def entails(self, form):
        #entails skal lave CNF resolution og hvis man får [] så true ellers false
        # #
        if not isinstance(form, belief):
            raise TypeError("Expected a belief instance")
        
        clauses = list()
        if len(self.beliefs) == 0:
            return False
        for CNFFormula in self.beliefs:
            clauses.extend(CNFFormula.b)
        
        clauses.extend(form.b)
                
        print(clauses, 'here')
        
        return self.CNFResolution(clauses)
            
    
    def contract(self, form):

        # form is a string (like from input), we convert and negate it
        negated_form = parse_and_cnf(form, neg=True)
        query_clauses = extractClauses(negated_form)

        new_beliefs = []
        for b in self.beliefs:
            # Build a temporary list of all beliefs *except* b
            kb_clauses = []
            for other in self.beliefs:
                if other != b:
                    kb_clauses.extend(other.b)
            # If that set of clauses does NOT entail the negated form, keep b
            if not CNFResolution(kb_clauses, query_clauses):
                new_beliefs.append(b)

        self.beliefs = new_beliefs
        return
    
    def CNFResolution(self, clauses):
        """
        Perform the CNF resolution algorithm to check if the clauses entail a contradiction.
        :param clauses: List of clauses (each clause is a list of literals).
        :return: True if a contradiction (empty clause) is found, False otherwise.
        """
        new = set()
        clauses = [frozenset(clause) for clause in clauses]  # Convert clauses to frozensets for immutability
        clauses_set = set(clauses)

        while True:
            # Generate all pairs of clauses
            pairs = combinations(clauses_set, 2)

            for (ci, cj) in pairs:
                resolvent = self.resolve(ci, cj)
                print(f"Resolving {ci} and {cj} to get {resolvent}")
                if frozenset() in resolvent:  # Check for empty clause
                    print("Contradiction found: Empty clause derived")
                    return True
                new.update(resolvent)

            # If no new clauses are generated, stop
            if new.issubset(clauses_set):
                print("No contradiction found")
                return False

            # Add new clauses to the set of clauses
            clauses_set.update(new)

    def resolve(self, ci, cj):
        """
        Resolve two clauses to produce resolvents.
        :param ci: Clause 1 (frozenset of literals).
        :param cj: Clause 2 (frozenset of literals).
        :return: Set of resolvent clauses.
        """
        resolvents = set()
        for literal in ci:
            if ~literal in cj:  # Check for complementary literals
                resolvent = (ci - {literal}) | (cj - {~literal})
                resolvents.add(frozenset(resolvent))
        return resolvents