class InnovationNumberGenerator:
    def __init__(self, start=0):
        """
        Constructor for the innovation number generator that is global for each genome
        :param start: Start the innovation number from this integer
        """
        self.innovation_number = start

    def next_int(self):
        """
        Retrieves the next innovation number for this instance
        :return:
        """
        self.innovation_number += 1
        return self.innovation_number
