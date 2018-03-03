class ConnectionGene:
    def __init__(self, in_node, out_node, weight, enabled, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation_number

    def __repr__(self):
        return "Connection: {}-->{} \tWeight: {}, Enabled: {}, Innovation Number: {}\n".format(self.in_node,
                                                                                               self.out_node,
                                                                                               self.weight,
                                                                                               self.enabled,
                                                                                               self.innovation_number)
