from qiskit import QuantumCircuit


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


# def simulator(QC, qNum=None, numshots=10000):
#     if qNum:
#         QC.measure(qNum, 0)
#     else:
#         QC.measure_all()
#     aer_sim = Aer.get_backend('aer_simulator', device='CPU')
#     transpiled = transpile(QC, aer_sim)
#     qobj = assemble(transpiled)
#     results = aer_sim.run(qobj, shots=numshots).result()
#     counts = results.get_counts()
#     return counts


gc = QuantumCircuit(4)
gc.h(0)
gc.h(1)
gc.h(2)
gc.cx([0, 1, 2], 3)
# gc.ccx(control_qubit1= 0, control_qubit2=1, target_qubit=2)
# gc.h(1)
# gc.h(1)
# gc.x(1)


# gc = init(gc, 3)
# gc = oracle(gc, 3)
# gc = diffuser(gc, 3)
print(gc)
# gc.draw()
# counts = simulator(gc)
# plot_histogram(counts, (10, 5))


from QASM_Processing import QASMProcessing
from MatrixGeneration import CircuitListToMatrix

qasm = QASMProcessing(gc)
# # cirData = qasm.stringProcessing()
# # cirData = qasm.listProcess
cirData = qasm.qasmToList()
print(cirData, len(cirData))

cirMat = CircuitListToMatrix(cirData, qasm.cirQubits)
matrix = cirMat.genMat

# print(matrix)


import numpy as np

ipVec = np.zeros(2 ** 4)
ipVec[0] = 1

print("\n\nfinal result:\n", np.matmul(ipVec, matrix))

