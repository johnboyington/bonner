
class Folding(object):
    
    def __init__(self, spectrum, response_functions):
        self.spectrum = self.set_spectrum(spectrum)
        self.response_functions = self.set_response_functions(response_functions)
        self.solutions = []
    
    def set_spectrum(self, spectrum):
        pass
    
    def set_response_functions(self, response_functions):
        pass
    
    def fold(self):
        pass
    
    def plot(self):
        pass
    
    def append_solution(self, sol):
        pass
    