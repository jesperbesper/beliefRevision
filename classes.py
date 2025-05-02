class belief:
    def __init__(self, b):
        self.b = b

    def __eq__(self, other):
        return self.b == other.b
    
class belief_base:
    def __init__(self):
        self.beliefs = set()

    def __iter__(self):
        return iter(self.beliefs)
    
    def __len__(self):
        return len(self.beliefs)
    
    def clear(self):
        self.beliefs = []


    def del_formula(self, form):
        for b in self.beliefs:
            if b.b == form:
                self.beliefs.remove(b)
                return
        return
    
    def add_belief(self, form):
        if not isinstance(form, belief):
            raise TypeError("Expected a belief instance")
        
        form = form.b
        form = cnf(form)
        self.del_formula(form)
 
        self.beliefs.append(belief(form))