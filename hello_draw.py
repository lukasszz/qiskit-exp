import qiskit
from PIL import Image
from qiskit.tools.visualization import matplotlib_circuit_drawer

qr = qiskit.QuantumRegister(1)
cr = qiskit.ClassicalRegister(1)
program = qiskit.QuantumCircuit(qr, cr)
program.measure(qr, cr)

image = matplotlib_circuit_drawer(program)

Image._show(image)