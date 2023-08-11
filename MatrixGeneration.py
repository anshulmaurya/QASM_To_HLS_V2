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
        elif gateName[0] == 'r':
            if gateName[1] == 'x':
                theta = eval(gateName[3:len(gateName) - 1])
                return np.matrix([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                                  [-1j * np.sin(theta / 2), np.cos(theta / 2)]])
            elif gateName[1] == 'y':
                theta = eval(gateName[3:len(gateName) - 1])
                return np.matrix([[np.cos(theta / 2) + 0j, -np.sin(theta / 2) + 0j],
                                  [np.sin(theta / 2) + 0j, np.cos(theta / 2) + 0j]])
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
            theta = eval(theta)
            phi = eval(phi)
            lam = eval(lam)
            return np.matrix([[np.cos(theta / 2), -1 * np.exp(1j * lam) * np.sin(theta / 2)],
                              [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + lam)) * np.cos(theta / 2)]])

    def cnotLayerMat(self, cnotDetail):
        import itertools
        tempCnotDetail = []
        for x in cnotDetail:
            if x != 'I':
                tempCnotDetail.append(x)
        cnotDetail = tempCnotDetail
        # del (tempCnotDetail)
        ctrl = cnotDetail[:len(cnotDetail) - 1]
        # ctrl.reverse()
        target = cnotDetail[len(cnotDetail) - 1]
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
            os.remove("./Circuit_Matrix.txt")
        except:
            pass
        f = open("Circuit_Matrix.txt", "a")
        # if self.type == 1:
        #     f2 = open("Type1_UpperPart.txt", "r")
        # if self.type == 2:
        #     f2 = open("Type2_UpperPart.txt", "r")
        # text = f2.read()
        # f2.close()
        # f.write(text)
        if self.check:
            cirMat = np.identity(2 ** self.number_of_qubit, dtype=complex)
        # layerMat = np.matrix(self.toGateMatrix(self.cirList[0]))
        layerMat = np.matrix([])
        pair = []
        cnotFlag = 0
        pairNum = 0
        print("Max Layers/Matrices: ", len(self.cirList) / self.number_of_qubit)
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
                        layerMat= np.round(layerMat, 2)
                if not self.check:
                    print(layerMat)
                    # s = "complex_t M" + str(pairNum) + "[] = {\n"
                    s = "{\n"
                    for r in layerMat:
                        for e in str(r):
                            if str(e) == "[" or str(e) == "]" or str(e) == " " or str(e) == "\n":
                                continue
                            l = len(s)
                            if e == '+' or e == '-' and s[l - 1] == ".":
                                e = '0' + e
                            if e == " " and s[l - 1] == ".":
                                # e = "0"
                                pass
                            if s[l - 1] == "i" or s[l - 2] == "i":
                                e = ", "
                            if 'j' in str(e):
                                e = e.replace("j", "i")
                            s = s + str(e)
                        s += "\n"
                    s += ",};\n\n\n\n"
                    f.write(s)

                if self.check:
                    check = self.is_unitary(layerMat)
                    print("Is Unitary: ", check)
                    print(layerMat)
                    cirMat = np.matmul(np.around(cirMat, 5), np.around(layerMat, 5))
                    if not check:
                        raise Exception("Non unitary Matrix")
                pair = []
        # # first computation block
        # if self.type == 1:
        #     f2 = open("Type1_MiddlePart.txt", 'r')
        # if self.type == 2:
        #     f2 = open("Type2_MiddlePart.txt", "r")
        # text = f2.read()
        # f2.close()
        # f.write(text)
        #
        # # 2nd and afterwards
        # if self.type == 1:
        #     for rep in range(2, pairNum):
        #         f2 = open("Type1_RepetitivePart.txt", 'r')
        #         text = f2.read()
        #         f2.close()
        #         newStr = "M" + str(rep) + "[i];//Mat"
        #         text = text.replace("M3[i];//Mat", newStr)
        #         f.write(text)
        #
        # if self.type == 2:
        #     for rep in range(5, pairNum, 4):
        #         print(rep)
        #         f2 = open("Type2_RepetitivePart.txt", 'r')
        #         text = f2.read()
        #         f2.close()
        #         newStr = "M" + str(rep) + "[i];//Mat"
        #         text = text.replace("M1[i];//Mat", newStr)
        #         newStr = "M" + str(rep+1) + "[i];//Mat"
        #         text = text.replace("M2[i];//Mat", newStr)
        #         newStr = "M" + str(rep+2) + "[i];//Mat"
        #         text = text.replace("M3[i];//Mat", newStr)
        #         newStr = "M" + str(rep+3) + "[i];//Mat"
        #         text = text.replace("M4[i];//Mat", newStr)
        #         f.write(text)
        #
        #
        # # Last Part
        # if self.type == 1:
        #     f2 = open("Type1_LastPart.txt", 'r')
        #     text = f2.read()
        #     newStr = "M" + str(pairNum) + "[i];//Mat"
        #     text = text.replace("M4[i];//Mat", newStr)
        #     f2.close()
        #     f.write(text)
        # if self.type == 2:
        #     f2 = open("Type2_LastPart.txt", 'r')
        #     text = f2.read()
        #     f2.close()
        #     newStr = "M" + str(pairNum) + "[i];//Mat"
        #     text = text.replace("M1[i];//Mat", newStr)
        #     newStr = "M" + str(pairNum+1) + "[i];//Mat"
        #     text = text.replace("M2[i];//Mat", newStr)
        #     newStr = "M" + str(pairNum+2) + "[i];//Mat"
        #     text = text.replace("M3[i];//Mat", newStr)
        #     newStr = "M" + str(pairNum+3) + "[i];//Mat"
        #     text = text.replace("M4[i];//Mat", newStr)
        #     f.write(text)
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
