import math
import time
from qiskit import QuantumCircuit, assemble
from qiskit.circuit.random import random_circuit
from qiskit_aer import Aer

from MatrixGeneration import CircuitListToMatrix
from QASM_Processing import QASMProcessing

EncodingAmplitudeAccuracy = 1

################################################################################################################################################################################
###############################################################################################################################################################################
################################################################################################################################################################################


n = 3
gc = QuantumCircuit(n)
for q in range(n):
    gc.h(q)

for q in range(n):
    gc.x(q)

gc.h(n-1)
gc.mct([n for n in range(n-1)], n-1)
gc.h(n-1)

for q in range(n):
    gc.x(q)

for q in range(n):
    gc.h(q)
for q in range(n):
    gc.x(q)
gc.h(n-1)
gc.mct([n for n in range(n-1)], n-1)
gc.h(n-1)
for q in range(n):
    gc.x(q)
for q in range(n):
    gc.h(q)

# gc = random_circuit(9, 1)

# for i in range(12):
#     for x in range(n):
#         gc.h(x)

print(gc)

print("Depth:=", gc.depth())

qasm = QASMProcessing(gc, transpiler=False)
# qasm = QASMProcessing('./QASM.txt', transpiler=True)
cirData = qasm.qasmToList()

cirMat = CircuitListToMatrix(cirData, qasm.cirQubits, check=True, type=1)
matrix = cirMat.genMat

print(matrix)

# TESTING WITH KET 0
import numpy as np

ipVec = np.zeros(2 ** n)
ipVec[0] = 1
# r = np.square(np.absolute(np.matmul(ipVec, matrix)))
r = np.matmul(ipVec, matrix)
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
