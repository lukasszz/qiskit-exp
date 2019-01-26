import sys
import numpy as np
import math

import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import CompositeGate
from qiskit import execute, register, available_backends

YEAST = "----------------------------------MM----------------------------"
PROTOZOAN = "--MM---------------M------------MMMM---------------M------------"
BACTERIAL = "---M---------------M------------MMMM---------------M------------"

YEAST = '10010010'
PROTOZOAN = '11010011'
BACTERIAL = '00000010'


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
    print()
    return qc


n = math.ceil(math.log2(len(YEAST))) + 1  # number of qubits
qr = QuantumRegister(n)
cr = ClassicalRegister(n)

qc_yeast = encode_bitstring(YEAST, qr, cr)
qc_protozoan = encode_bitstring(PROTOZOAN, qr, cr)
qc_bacterial = encode_bitstring(BACTERIAL, qr, cr)

circs = {"YEAST": qc_yeast, "PROTOZOAN": qc_protozoan, "BACTERIAL": qc_bacterial}

inverse_qc_yeast = encode_bitstring(YEAST, qr, cr, inverse=True)
inverse_qc_protozoan = encode_bitstring(PROTOZOAN, qr, cr, inverse=True)
inverse_qc_bacterial = encode_bitstring(BACTERIAL, qr, cr, inverse=True)

inverse_circs = {"YEAST": inverse_qc_yeast, "PROTOZOAN": inverse_qc_protozoan,
                 "BACTERIAL": inverse_qc_bacterial}


key = "PROTOZOAN"  # the name of the code used as key to find similar ones

# use local simulator
qiskit.IBMQ.load_accounts()
backend = qiskit.backends.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))

shots = 1000

combined_circs = {}
count = {}

most_similar, most_similar_score = "", -1.0

for other_key in inverse_circs:
    if other_key == key:
        continue

    combined_circs[other_key] = circs[key] + inverse_circs[
        other_key]  # combined circuits to look for similar codes
    job = execute(combined_circs[other_key], backend=backend, shots=shots)
    st = job.result().get_counts(combined_circs[other_key])
    if "0" * n in st:  # DLACZEGO ODCZYTYWANA JEST WARTOSC TEGO STANU? DLACZEGO STAN 0000 MA ZNACZENIE? CZY NIE POWINNO SIĘ SPRAWDZIĆ WSZYSTKICH
        sim_score = st["0" * n] / shots
    else:
        sim_score = 0.0

    print("Similarity score of", key, "and", other_key, "is", sim_score)
    if most_similar_score < sim_score:
        most_similar, most_similar_score = other_key, sim_score

print("[ANSWER]", key, "is most similar to", most_similar)
