import sys
import numpy as np
import math

import qiskit
from PIL import Image
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import CompositeGate
from qiskit import execute, register, available_backends
from qiskit.tools.visualization import matplotlib_circuit_drawer, plot_histogram


def encode_bitstring(bitstring, qr, cr, inverse=False):
    """
    create a circuit for constructing the quantum superposition of the bitstring
    """
    n = math.ceil(math.log2(len(bitstring))) + 1  # number of qubits
    assert n > 2, "the length of bitstring must be at least 2"

    qc = QuantumCircuit(qr, cr)

    # the probability amplitude of the desired state
    desired_vector = np.array([0.0 for i in range(2 ** n)])  # initialize to zero
    amplitude = np.sqrt(1.0 / 2 ** (n - 1))

    for i, b in enumerate(bitstring):
        pos = i * 2
        if b == "1" or b == "M":
            pos += 1
        desired_vector[pos] = amplitude
    if not inverse:
        qc.initialize(desired_vector, [qr[i] for i in range(n)])
        qc.barrier(qr)
    else:
        qc.initialize(desired_vector, [qr[i] for i in range(n)]).inverse()  # invert the circuit
        for i in range(n):
            qc.measure(qr[i], cr[i])
    print('bitstring: %s, no. of cubits: %s Desired vecotr [%s]:\n%s ' % (
        bitstring, n, len(desired_vector), desired_vector))
    return qc


YEAST = "----------------------------------MM----------------------------"

# bs1 = '0101'


bs1 = '10010010'
bs2 = '11010011'
bs3 = '00000010'

bs1 = "----------------------------------MM----------------------------"
bs2 = "--MM---------------M------------MMMM---------------M------------"
bs3 = "---M---------------M------------MMMM---------------M------------"

n = math.ceil(math.log2(len(bs1))) + 1  # number of qubits
qr = QuantumRegister(n)
cr = ClassicalRegister(n)

# Why we use the same qr for all the bitstrings?
# Is this this magic of qunatum, that the kubit can be in various states at the same time?
# TODO: Debuti if it is the same object?
# Yes! All the bistrings are stored in the same Quantum register. How are they distingused?
# By quantum Circut?
# MAYBE start to read the state afeter INIT?????
qc1 = encode_bitstring(bs1, qr, cr)
qc2 = encode_bitstring(bs2, qr, cr)
qc3 = encode_bitstring(bs3, qr, cr)

circs = {'bs1': qc1, 'bs2': qc2, 'bs3': qc3}

qc1i = encode_bitstring(bs1, qr, cr, inverse=True)
qc2i = encode_bitstring(bs2, qr, cr, inverse=True)
qc3i = encode_bitstring(bs3, qr, cr, inverse=True)

circs_inv = {'bs1': qc1i, 'bs2': qc2i, 'bs3': qc3i}

key = 'bs1'

combined_circs = {}
count = {}

most_simialr, most_simial_score = "", -1.0

qiskit.IBMQ.load_accounts()
backend = qiskit.backends.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))
shots = 1000

for other_key in circs_inv:
    if other_key == key:
        continue

    combined_circs[other_key] = circs[key] + circs_inv[
        other_key]  # comined circuits to look for simialr codes
    job = execute(combined_circs[other_key], backend=backend, shots=shots)
    st = job.result().get_counts(combined_circs[other_key])

    if "0" * n in st:
        sim_score = st["0" * n] / shots
    else:
        sim_score = 0

    print("Similarity score fo ", key, " and ", other_key, " is ", sim_score)

# qiskit.IBMQ.load_accounts()
# backend = qiskit.backends.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))
# qcc = qc2 + qc1i
# job = execute(qcc, backend=backend)
# stat = job.result().get_counts(qcc)
# print(stat)
# plot_histogram(stat)

# image = matplotlib_circuit_drawer(qc)
# Image._show(image)
