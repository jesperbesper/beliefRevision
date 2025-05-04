from itertools import chain, combinations

class belief:
    def __init__(self, b):
        self.b = b
        self.prio = 0

    def __eq__(self, other):
        return self.b == other.b
    
    def __str__(self):
        return str(self.b) 
    
    def __repr__(self):
        return f"belief({repr(self.b)})" 
    
    def incrementPrio(self):
        return self.prio + 1
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
    
    def increment_prio(self):
        for b in self.beliefs:
            b.prio = b.incrementPrio()
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
                
        # print(clauses, 'here')
        
        return self.CNFResolution(clauses)
            
    
    def contract(self, form):
        """
        Remove any beliefs that contradict the given formula, retaining the maximal subset of consistent beliefs.
        :param form: The belief to contract against (in CNF form).
        """
        def is_consistent(belief_subset):
            """
            Check if a subset of beliefs is consistent with the given formula.
            """
            kb_clauses = []
            for belief in belief_subset:
                kb_clauses.extend(belief.b)
            kb_clauses.extend(form.b)
            return not self.CNFResolution(kb_clauses)

        # Generate all subsets of the belief base
        all_subsets = chain.from_iterable(combinations(self.beliefs, r) for r in range(len(self.beliefs) + 1))

        # Find the largest consistent subset
        maximal_subset = []
        for subset in all_subsets:
            if is_consistent(subset) and len(subset) > len(maximal_subset):
                maximal_subset = subset

        # Update the belief base with the maximal consistent subset
        self.beliefs = list(maximal_subset)
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
                # print(f"Resolving {ci} and {cj} to get {resolvent}")
                if frozenset() in resolvent:  # Check for empty clause
                    # print("Contradiction found: Empty clause derived")
                    return True
                new.update(resolvent)

            # If no new clauses are generated, stop
            if new.issubset(clauses_set):
                # print("No contradiction found")
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