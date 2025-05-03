from cli import parse_and_cnf, extractClauses
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

    def __iter__(self):
        return iter(self.beliefs)
    
    def __len__(self):
        return len(self.beliefs)
    
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
        self.CNFResolution(clauses)
        return False
            
    
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
        # her skal vi lave CNF resolution
        return