# this file takes the qiskit circuit object and processes the QASM and
# provides circuit data in a list of tuples; (gateType, Pos)
import math as m
from typing import Any
from qiskit import transpile


class QASMProcessing:
    def __init__(self, quantumCircuit, transpiler=True):
        if "qiskit.circuit." in str(type(quantumCircuit)):
            if transpiler:
                quantumCircuit = transpile(quantumCircuit, basis_gates=['u', 'id', 'cx', 'sx',
                                                                        't', 'x', 'h', 'z', 'rx', 'ry', 'rz'])
            qASM = quantumCircuit.qasm()
            print("Transpiled Circuit Depth: ", quantumCircuit.depth())
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
            file1 = open(quantumCircuit, 'r')
            self.Lines = file1.readlines()
            file1.close()
            for l in self.Lines:
                if "qreg" in l:
                    Nqubit = ""
                    for s in l[7:]:
                        if s == "]":
                            break
                        Nqubit += s
                    self.numberOfQubits = int(Nqubit, 10)
            self.circuitData = []

    def stringProcessing(self):
        count = 0
        for l in self.Lines:
            if "OPENQASM" in l or "include" in l or "barrier" in l or "qreg" in l or "creg" in l:
                continue
            # counts loop iteration
            count += 1

            # code to extract gate type and1 position
            spcaeIndex = l.index(' ')
            gate = l[:spcaeIndex]
            spcaeIndex = len(gate)
            if gate == "ccx" or gate == "cx" or "cp" in gate:
                if gate == "cx":
                    l = 'c' + l  # making cx gate as ccx (are same)
                    # print(l)
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
                try:
                    gatePos = int(l[spcaeIndex + 3:len(l) - 3])
                except:
                    pass
                    raise Exception("Turn on the transpiler -- Non supported gate", gate)

            self.circuitData.append((gate, gatePos))
            # print(gate, gatePos)
        return self.circuitData

    def qasmToList(self):
        cirData: list[Any] = self.stringProcessing()
        print(cirData)
        finalList = []
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
                        r += self.numberOfQubits  # remove -1 in case of failure
                    for ite in range(r):
                        finalList.append('I')
                        n += 1
                    finalList.append(x[0])
                    n += 1
                    continue
        # print(finalList)

        if len(finalList) % self.numberOfQubits != 0:
            itr = (m.ceil(len(finalList) / self.numberOfQubits) * self.numberOfQubits) - len(finalList)
            for _ in range(itr):
                finalList.append('I')

        # for index, g in enumerate(finalList):
        #     if 'cx' in g or 'ccx' in g:
        #         for n in range(self.numberOfQubits):
        #             if n in finalList[index][1]:
        #
        self.circuitData = finalList
        return self.circuitData

    @property
    def cirQubits(self):
        return self.numberOfQubits

