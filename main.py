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

# gc = QuantumCircuit(n)
# for x in range(n):
#     gc.h(x)
# for x in range(n):
#     gc.z(x)
# gc.cx(1,2)
# gc = oracle(gc, n, ["10100"])
# gc = diffuser(gc, n)


# pi = 180
# def qft_rotations(circuit, n):
#     """Performs qft on the first n qubits in circuit (without swaps)"""
#     if n == 0:
#         return circuit
#     n -= 1
#     circuit.h(n)
#     for qubit in range(n):
#         circuit.cp(pi/2**(n-qubit), qubit, n)
#     # At the end of our function, we call the same function again on
#     # the next qubits (we reduced n by one earlier in the function)
#     qft_rotations(circuit, n)
#
# def swap_registers(circuit, n):
#     for qubit in range(n//2):
#         circuit.swap(qubit, n-qubit-1)
#     return circuit
#
# def qft(circuit, n):
#     """QFT on the first n qubits in circuit"""
#     qft_rotations(circuit, n)
#     swap_registers(circuit, n)
#     return circuit

n = 9
gc  = QuantumCircuit(n)
# qft(gc,n)

# gc = random_circuit(9, 1)
for x in range(n):
    gc.h(x)
print(gc)

print("Depth:=", gc.depth())

qasm = QASMProcessing(gc, transpiler=True)
# qasm = QASMProcessing('./QASM.txt', transpiler=True)
cirData = qasm.qasmToList()

cirMat = CircuitListToMatrix(cirData, qasm.cirQubits, check=False, type=1)
matrix = cirMat.genMat

print(matrix)

## TESTING WITH KET 0
# import numpy as np
#
# ipVec = np.zeros(2 ** n)
# ipVec[0] = 1
# r = np.square(np.absolute(np.matmul(ipVec, matrix)))
# print("\n\nfinal result:\n")
# print(r)



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
