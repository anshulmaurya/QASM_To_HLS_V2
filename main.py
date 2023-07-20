from qiskit import QuantumCircuit
from QASM_Processing import QASMProcessing
from MatrixGeneration import CircuitListToMatrix

def init(cir, n):
    for p in range(n):
        cir.h(p)
        # cir.barrier(p)
    return cir


def oracle(cir, n):
    # 001
    # cir.x(0)
    cir.x(1)
    cir.h(2)
    cir.mct([0, 1], 2)
    cir.h(2)
    cir.x(1)
    # cir.x(0)
    # cir.barrier([0, 1, 2])

    # # 100
    # cir.x(0)
    # cir.x(1)
    # cir.h(2)
    # cir.mct([0, 1], 2)
    # cir.h(2)
    # cir.x(1)
    # cir.x(0)
    # cir.barrier([0, 1, 2])
    return cir

def diffuser(cir, n):
    for p in range(n):
        cir.h(p)
    for p in range(n):
        cir.x(p)

    cir.h(2)
    cir.mct([x for x in range(n - 1)], n - 1)
    cir.h(2)

    for p in range(n):
        cir.x(p)
    for p in range(n):
        cir.h(p)
    return cir

gc = QuantumCircuit(3)
gc = init(gc, 3)
gc = oracle(gc, 3)
gc = diffuser(gc, 3)
print(gc)


qasm = QASMProcessing(gc)
cirData = qasm.qasmToList()
print(cirData, len(cirData))

cirMat = CircuitListToMatrix(cirData, qasm.cirQubits)
matrix = cirMat.genMat




# TESTING WITH KET 0
import numpy as np

ipVec = np.zeros(2 ** 3)
ipVec[0] = 1

print("\n\nfinal result:\n", np.matmul(ipVec, matrix))

