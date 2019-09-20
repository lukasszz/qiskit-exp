from qiskit import QuantumRegister, QuantumCircuit, execute, Aer
from qiskit.circuit import ClassicalRegister

backend = Aer.get_backend('qasm_simulator')

QR = QuantumRegister(1)
CR = ClassicalRegister(1)
QC = QuantumCircuit(QR, CR)


QC.h(QR)
QC.x(QR)
QC.h(QR)

QC.measure(QR, CR)

job = execute(QC, backend=backend, shots=1024)
st = job.result().get_counts()
print(st)