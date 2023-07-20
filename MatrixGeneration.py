import numpy as np


class CircuitListToMatrix:
    def __init__(self, cirList, number_of_qubit):
        if len(cirList) == 0:
            raise Exception("empty list cant find circuit data")
        self.cirList = cirList
        self.number_of_qubit = number_of_qubit

    def toGateMatrix(self, gateName):
        if gateName == 'h':
            return np.matrix('0.707 0.707;'
                             '0.707 -0.707')
        elif gateName == 'I':
            return np.matrix('1 0; '
                             '0 1')
        elif gateName == 'x':
            return np.matrix('0 1;'
                             '1 0')


    @property
    def genMat(self):
        cirMat = np.identity(2**self.number_of_qubit)
        # layerMat = np.matrix(self.toGateMatrix(self.cirList[0]))
        layerMat = np.matrix([])
        m = []
        for n in range(0, len(self.cirList), self.number_of_qubit):
            pair = self.cirList[n:n + self.number_of_qubit]
            if len(pair) == self.number_of_qubit:
                print(pair, "  ")
                for pos, g in enumerate(pair):
                    if pos == 0:
                        layerMat = self.toGateMatrix(g)
                        continue
                    layerMat = np.kron(self.toGateMatrix(g), layerMat)
                cirMat = np.matmul(cirMat, layerMat)
        return cirMat
