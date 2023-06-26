# this file takes the qiskit circuit object and processes the QASM and
# provides circuit data in a list of tuples; (gateType, Pos)
from typing import List, Any

import qiskit


class QASMProcessing():
    def __init__(self, quantumCircuit):
        if "qiskit.circuit." in str(type(quantumCircuit)):
            qASM = quantumCircuit.qasm()
            file1 = open('./QASM.txt', 'w+')
            file1.writelines(qASM)
            file1.close()
            file1 = open('./QASM.txt', 'r')
            self.Lines = file1.readlines()
            file1.close()
            self.numberOfQubits = quantumCircuit.num_qubits
            self.circuitData = []
            self.QV = quantumCircuit.depth() * quantumCircuit.num_qubits
        else:
            raise Exception("invalid circuit object", quantumCircuit)

    def stringProcessing(self):
        count = 0
        for l in self.Lines:
            if "OPENQASM" in l or "include" in l or "barrier" in l or "qreg" in l:
                continue
            # counts loop iteration
            count += 1

            # code to extract gate type and1 position
            spcaeIndex = l.index(' ')
            gate = l[:spcaeIndex]
            if gate == "ccx":
                ccxGatePos = []
                numStr = ''
                flag = 0
                for num, ch in enumerate(l):
                    if ch == "]":
                        flag = 0
                        ccxGatePos.append(int(numStr))
                        numStr = ''
                    if flag == 1:
                        numStr += ch

                    if ch == "[":
                        flag = 1
                gatePos = ccxGatePos
            else:
                gatePos = int(l[spcaeIndex + 3:len(l) - 3])
            self.circuitData.append((gate, gatePos))
            # print(gate, gatePos)
        return self.circuitData

    def listProcessing(self):
        cirData: list[Any] = self.stringProcessing()
        cirData.reverse()
        print(cirData)
        finalList = []
        # print(finalList)
        curr = 0
        n = 0
        for x in cirData:
            if n % self.numberOfQubits == 0:
                n = 0
            if x[1] == n:
                finalList.append(x[0])
                n += 1
                continue
            else:
                pos = x[1]
                if type(x[1]) == list:
                    # pos = x[1][0]
                    finalList.append(x)
                    n += (len(x[1]))
                    continue
                else:
                    r = pos - n
                    if r < 0:
                        r += self.numberOfQubits-1    # remove +1 in case of failure
                    for ite in range(r):
                        finalList.append('I')
                        n += 1
                    finalList.append(x[0])
                    n += 1
                    continue
        # print(finalList)
        self.circuitData = finalList
        return self.circuitData

    #
    # @property
    # def listProcess(self):
    #     cirData: list[Any] = self.stringProcessing()
    #     lenCount = 0
    #     for g in cirData:
    #         if g[0] == "ccx":
    #             lenCount += len(g[1])
    #         else:
    #             lenCount += 1
    #
    #     finalList = [[] for _ in range(lenCount + 1)]
    #     curr = 0
    #     n = 0
    #     for info in cirData:
    #         if n % self.numberOfQubits == 0:
    #             curr = n
    #         if info[0] != 'ccx':
    #             # print(curr + int(info[1]))
    #             finalList[curr + int(info[1])].append(info[0])
    #         else:
    #             # pass
    #             for i in range(len(info[1])):
    #                 if n % self.numberOfQubits == 0:
    #                     curr = n
    #                 if i == len(info[1]) - 1:
    #                     finalList[curr + info[1][i]].append('cx')
    #                 else:
    #                     finalList[curr + info[1][i]].append('c')
    #                     n += 1
    #         n += 1
    #     return finalList