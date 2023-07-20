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

    def cnotLayerMat(self, cnotDetail):
        import itertools
        for index, x in enumerate(cnotDetail):
            if x == 'I':
                cnotDetail.pop(index)

        sqs = [''.join(s) for s in list(itertools.product(*[['0', '1']] * (self.number_of_qubit)))]

        print('cnotdetail:', cnotDetail, sqs)

        return []

    @property
    def genMat(self):
        cirMat = np.identity(2 ** self.number_of_qubit)
        # layerMat = np.matrix(self.toGateMatrix(self.cirList[0]))
        layerMat = np.matrix([])
        pair = []
        cnotFlag = 0
        for num in range(len(self.cirList)):
            if 'cx' in self.cirList[num] or 'ccx' in self.cirList[num]:
                cnotFlag = 1
                pair = self.cirList[num][1]
                while len(pair) != self.number_of_qubit:
                    pair.append('I')
            else:
                pair.append(self.cirList[num])
            if len(pair) == self.number_of_qubit:
                print(pair, "  ")
                if cnotFlag == 1:
                    cnotFlag = 0
                    # layerMat = self.cnotLayerMat(pair)
                    self.cnotLayerMat(pair)
                    pass
                else:
                    for pos, g in enumerate(pair):
                        if pos == 0:
                            layerMat = self.toGateMatrix(g)
                            continue
                        layerMat = np.kron(self.toGateMatrix(g), layerMat)
                cirMat = np.matmul(cirMat, layerMat)
                pair = []
        return cirMat
