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
        
        for b in self.beliefs:
            if b == form:
                return True
        return False
    
    def contract(self, form):
        # her skal vi fjerne de formulas som contradicter form