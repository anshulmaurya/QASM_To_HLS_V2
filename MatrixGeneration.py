import numpy as np


class CircuitListToMatrix:
    def __init__(self, cirList, number_of_qubit, check = False):
        if len(cirList) == 0:
            raise Exception("empty list cant find circuit data")
        self.cirList = cirList
        self.number_of_qubit = number_of_qubit
        self.check = check

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
        tempCnotDetail = []
        for x in cnotDetail:
            if x != 'I':
                tempCnotDetail.append(x)
        cnotDetail = tempCnotDetail
        del(tempCnotDetail)
        ctrl = cnotDetail[:len(cnotDetail) - 1]
        # ctrl.reverse()
        target = cnotDetail[len(cnotDetail) - 1]
        sqs = [''.join(s) for s in list(itertools.product(*[['0', '1']] * self.number_of_qubit))]
        CNOT_LayerArray = np.zeros((2 ** self.number_of_qubit, 2 ** self.number_of_qubit))
        for i, binSeq in enumerate(sqs):
            ctrlFlag = 0
            for c in ctrl:
                if binSeq[c] == '1':
                    ctrlFlag = 1
                else:
                    ctrlFlag = 0
                    break
            if ctrlFlag == 1:
                s = ''
                if binSeq[target] == '1':
                    for pos, ch in enumerate(binSeq):
                        if pos == target:
                            ch = '0'
                        s = s + ch
                else:
                    for pos, ch in enumerate(binSeq):
                        if pos == target:
                            ch = '1'
                        s = s + ch
                r = sqs.index(s)
                CNOT_LayerArray[r][i] = 1
            else:
                CNOT_LayerArray[i][i] = 1
        # print('cnotdetail:', CNOT_LayerArray)
        return CNOT_LayerArray

    @property
    def genMat(self):
        if self.check:
            cirMat = np.identity(2 ** self.number_of_qubit)
        # layerMat = np.matrix(self.toGateMatrix(self.cirList[0]))
        layerMat = np.matrix([])
        pair = []
        cnotFlag = 0
        pairNum = 0
        for num in range(len(self.cirList)):
            if 'cx' in self.cirList[num] or 'ccx' in self.cirList[num]:
                cnotFlag = 1
                pair = self.cirList[num][1]
                while len(pair) != self.number_of_qubit:
                    pair.append('I')
            else:
                pair.append(self.cirList[num])
                try:
                    if 'cx' in self.cirList[num + 1] or 'ccx' in self.cirList[num + 1]:
                        while len(pair) != self.number_of_qubit:
                            pair.append('I')
                except:
                    pass

            if len(pair) == self.number_of_qubit:
                pairNum += 1
                print(f"\nPAIR {pairNum}:", pair, "  ")
                if cnotFlag == 1:
                    cnotFlag = 0
                    layerMat = np.matrix(self.cnotLayerMat(pair))
                    # self.cnotLayerMat(pair)
                    # pass
                else:
                    for pos, g in enumerate(pair):
                        if pos == 0:
                            layerMat = self.toGateMatrix(g)
                            continue
                        layerMat = np.kron(layerMat, self.toGateMatrix(g))
                print(layerMat)

                if self.check:
                    check = self.is_unitary(layerMat)
                    print("Is Unitary: ", check)
                    print(layerMat)
                    cirMat = np.matmul(np.around(cirMat, 3), np.around(layerMat, 3))
                pair = []
        if self.check:
            check = self.is_unitary(layerMat)
            print("\nIs Unitary: ", check)
            print("Final matrix for circuit: \n", cirMat)
            return cirMat
        else:
            return True

    @staticmethod
    def is_unitary(m):
        # m = np.around(m, 1)
        return np.allclose(np.eye(m.shape[0]), np.around(m.H * m, 2))

