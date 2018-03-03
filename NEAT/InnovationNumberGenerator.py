class InnovationNumberGenerator:
    def __init__(self, start=0):
        self.innovation_number = start

    def next_int(self):
        self.innovation_number += 1
        return self.innovation_number
