import numpy as np
import os

class CircuitListToMatrix:
    def __init__(self, cirList, number_of_qubit, check=True, type=1):
        if len(cirList) == 0:
            raise Exception("empty list cant find circuit data")
        self.cirList = cirList
        self.number_of_qubit = number_of_qubit
        self.check = check
        self.type = type

    def toGateMatrix(self, gateName):
        gateName = gateName.replace("pi", "180")
        if gateName == 'h':
            return np.matrix([[0.707 + 0.j, 0.707 + 0.j],
                              [0.707 + 0.j, -0.707 + 0.j]])
        elif gateName == 'I':
            return np.matrix([[1.0 + 0.j, 0. + 0.j],
                              [0. + 0.j, 1.0 + 0.j]])
        elif gateName == 'x':
            return np.matrix([[0.0 + 0.j, 1. + 0.j],
                              [1. + 0.j, 0. + 0.j]])
        elif gateName == 'z':
            return np.matrix([[1.0 + 0.j, 0. + 0.j],
                              [0. + 0.j, -1.0 + 0.j]])
        elif gateName == 's':
            return np.matrix([[1.0 + 0.j, 0. + 0.j],
                              [0. + 0.j, 0.0 + 1.j]])
        elif gateName == 't':
            return np.matrix([[1, 0],
                              [0, (np.cos(45) + (np.sin(45) * 1j))]])  # pi/4
        elif gateName == 'sx':
            return np.matrix([[1 + 1j, 1 - 1j],
                              [1 - 1j, 1 + 1j]])
        elif gateName == 'id':
            return np.matrix([[1 + 0j, 0 + 0j],
                              [0 + 0j, 1 + 0j]])
        elif gateName[0] == 'r':
            if gateName[1] == 'x':
                theta = eval(gateName[3:len(gateName) - 1]) / 2
                return np.matrix([[np.cos(theta), -1j * np.sin(theta)],
                                  [-1j * np.sin(theta), np.cos(theta)]])
            elif gateName[1] == 'y':
                theta = eval(gateName[3:len(gateName) - 1]) / 2
                return np.matrix([[np.cos(theta) + 0j, -np.sin(theta) + 0j],
                                  [np.sin(theta) + 0j, np.cos(theta) + 0j]])
            elif gateName[1] == 'z':
                lam = eval(gateName[3:len(gateName) - 1]) / 2
                return np.matrix([[np.exp(-1j * lam), 0],
                                  [0, np.exp(1j * lam)]])

        elif gateName[0] == 'u':
            gateName = gateName[2:len(gateName) - 1]
            theta = ""
            phi = ""
            lam = ""
            comaFlag = 0
            for ch in gateName:
                if ch == ',':
                    comaFlag += 1
                    continue
                if comaFlag == 0:
                    theta = theta + ch
                if comaFlag == 1:
                    phi = phi + ch
                if comaFlag == 2:
                    lam = lam + ch
            theta = eval(theta) / 2
            phi = eval(phi)
            lam = eval(lam)
            return np.matrix([[np.cos(theta), -1 * np.exp(1j * lam) * np.sin(theta)],
                              [np.exp(1j * phi) * np.sin(theta), np.exp(1j * (phi + lam)) * np.cos(theta)]])

    def cnotLayerMat(self, cnotDetail):
        import itertools
        tempCnotDetail = []
        for x in reversed(cnotDetail):
            if x != 'I':
                tempCnotDetail.append(x)
        cnotDetail = tempCnotDetail
        del (tempCnotDetail)
        ctrl = cnotDetail[:len(cnotDetail) - 1]
        # ctrl.reverse()
        target = cnotDetail[len(cnotDetail) - 1]
        print("ctrl: ", ctrl, target)
        sqs = [''.join(s) for s in list(itertools.product(*[['0', '1']] * self.number_of_qubit))]
        CNOT_LayerArray = np.zeros((2 ** self.number_of_qubit, 2 ** self.number_of_qubit), dtype=complex)
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
                CNOT_LayerArray[r][i] = 1 + 0.j
            else:
                CNOT_LayerArray[i][i] = 1 + 0.j
        # print('cnotdetail:', CNOT_LayerArray)
        return CNOT_LayerArray

    @property
    def genMat(self):
        try:
            os.remove("./matrix.txt")
        except:
            pass
        f = open("matrix.txt", "a")
        if self.check:
            cirMat = np.identity(2 ** self.number_of_qubit, dtype=complex)
            ipVec = np.zeros(2 ** self.number_of_qubit)
            ipVec[0] = 1
        # layerMat = np.matrix(self.toGateMatrix(self.cirList[0]))
        layerMat = np.matrix([])
        pair = []
        cnotFlag = 0
        pairNum = 0
        # print("Max Layers/Matrices: ", len(self.cirList) / self.number_of_qubit)
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
                        layerMat = np.round(np.kron(self.toGateMatrix(g), layerMat), 3)
                        # layerMat = np.kron(layerMat, self.toGateMatrix(g))
                        if not self.check:
                            layerMat = layerMat.tolist()
                if not self.check:
                    # print(layerMat)
                    s = "{\n"
                    for r in layerMat:
                        for e in str(r):
                            if e.isnumeric() == True or e in "+-.j":
                                l = len(s)
                                if e == '.' and s[l - 1] == ".":
                                    continue
                                if e == '+' or e == '-' and s[l - 1] == ".":
                                    # e = '0' + e
                                    pass
                                if e == " " and s[l - 1] == ".":
                                    e = "0"
                                if s[l - 1] == "i" or s[l - 2] == "i":
                                    e = ", " + e
                                if e == 'j':
                                    e = 'i'
                                s = s + str(e)
                            # else:
                            #     pass
                        s += "\n"
                    s += ",};\n\n\n\n"
                    f.write(s)

                if self.check:
                    check = self.is_unitary(layerMat)
                    print("Is Unitary: ", check)
                    print("\n*** Layer Matrix: \n", layerMat)
                    r = np.matmul(ipVec, layerMat)
                    print("Output Statevector:\n", r)
                    ipVec = r
                    cirMat = np.matmul(np.around(cirMat, 5), np.around(layerMat, 5))
                    print("\n*** Circuit Matrix: \n", cirMat)
                    if not check:
                        raise Exception("Non unitary Matrix")
                pair = []
        f.close()
        if self.check:
            check = self.is_unitary(layerMat)
            print("\nIs Unitary: ", check)
            print("Final matrix for circuit: \n", cirMat)
            return cirMat
        else:
            return True

    @staticmethod
    def is_unitary(m):
        return np.allclose(np.eye(m.shape[0]), np.around(m.H * m, 2))
