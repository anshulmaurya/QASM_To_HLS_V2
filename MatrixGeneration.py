import numpy as np

class CircuitListToMatrix:
    def __init__(self, cirList, number_of_qubit):
        if len(cirList) == 0:
            raise Exception("empty list cant find circuit data")
        self.cirList = cirList
        self.number_of_qubit = number_of_qubit


    @property
    def genMat(self):
        # matOnEachWire = np.matrix([[None] ])
        cirMat = np.matrix([])

        for n in range(0, len(self.cirList), 3):
            pair = self.cirList[n:n+3]
            print(pair, "  ")


        return cirMat
