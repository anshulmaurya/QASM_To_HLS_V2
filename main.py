from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


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


def simulator(QC, qNum=None, numshots=10000):
    if qNum:
        QC.measure(qNum, 0)
    else:
        QC.measure_all()
    aer_sim = Aer.get_backend('aer_simulator', device='CPU')
    transpiled = transpile(QC, aer_sim)
    qobj = assemble(transpiled)
    results = aer_sim.run(qobj, shots=numshots).result()
    counts = results.get_counts()
    return counts


gc = QuantumCircuit(3)
gc = init(gc, 3)
gc = oracle(gc, 3)
gc = diffuser(gc, 3)
print(gc)
# gc.draw()
# counts = simulator(gc)
# plot_histogram(counts, (10, 5))


from QASM_Processing import QASMProcessing

qasm = QASMProcessing(gc)
cirData = qasm.stringProcessing()
# cirData = qasm.listProcess
cirData = qasm.qasmToList()

print(cirData, len(cirData))

if len(cirData) % 3 == 0:
    print("True")
else:
    print("False")
