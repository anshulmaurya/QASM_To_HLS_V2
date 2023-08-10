import math
from qiskit.circuit.random import random_circuit
from MatrixGeneration import CircuitListToMatrix
from QASM_Processing import QASMProcessing

EncodingAmplitudeAccuracy = 1


def oracle(oracleCir, numQubits, winState):
    qubitList = [x for x in range(numQubits)]
    m = math.floor(
        3.14 * EncodingAmplitudeAccuracy / (4 * (math.asin(math.sqrt(len(winState) / math.pow(2, len(qubitList)))))))
    print("Circuit Repetetion = ", m)
    if m == 0:
        raise Exception("circuit not possible")
    # final_oracleCir = QuantumCircuit(len(qubitList))
    # oracleCir = QuantumCircuit(len(qubitList))
    for n in range(numQubits):
        oracleCir.h(n)
    exeCount = 0
    for ws in winState:
        exeCount += 1
        if len(ws) != len(qubitList):
            raise Exception("invalid state with respect to the number of qubits")
        # if exeCount > 1:
        qPos = 0
        for bit in ws:
            if bit == '0':
                oracleCir.x(len(qubitList) - 1 - qPos)
            qPos += 1
        oracleCir.h(len(qubitList) - 1)
        nq = len(qubitList)
        oracleCir.mct(list(range(nq - 1)), nq - 1)  # multi-controlled-toffoli
        oracleCir.h(len(qubitList) - 1)
        qPos = 0
        for bit in ws:
            if bit == '0':
                oracleCir.x(len(qubitList) - 1 - qPos)
            qPos += 1

    return oracleCir


# n-bit generelized diffuser from quiskit git
def diffuser(qc, qubitList):
    nqubits = qubitList
    # qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits - 1)
    qc.mct(list(range(nqubits - 1)), nqubits - 1)  # multi-controlled-toffoli
    qc.h(nqubits - 1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    return qc


################################################################################################################################################################################
###############################################################################################################################################################################
################################################################################################################################################################################

n = 5
# gc = QuantumCircuit(n)
# gc = oracle(gc, n, ["10100"])
# gc = diffuser(gc, n)

gc = random_circuit(n, 10)

print(gc)
print("Depth:=", gc.depth())

qasm = QASMProcessing(gc)
# qasm = QASMProcessing('./QASM.txt', transpiler=True)
cirData = qasm.qasmToList()

cirMat = CircuitListToMatrix(cirData, qasm.cirQubits, check=False)
matrix = cirMat.genMat

print(matrix)

## TESTING WITH KET 0
import numpy as np

ipVec = np.zeros(2 ** n)
ipVec[0] = 1
r = np.square(np.absolute(np.matmul(ipVec, matrix)))
print("\n\nfinal result:\n")
print(r)

# circuit already defined
# from qiskit import*
#
# gc = random_circuit(2, 2)
# backend = Aer.get_backend('unitary_simulator')
# job = execute(gc, backend)
# result = job.result()
# matrix = result.get_unitary(gc, decimals=2)
# print(result.get_unitary(gc, decimals=2))
#
# import numpy as np
#
# ipVec = np.zeros(2 ** 2)
# ipVec[0] = 1
#
# print("\n\nfinal result:\n", np.matmul(ipVec, matrix))

