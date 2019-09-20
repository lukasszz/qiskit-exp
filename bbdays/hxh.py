from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

if __name__ == '__main__':
    backend = Aer.get_backend('qasm_simulator')
    q = QuantumRegister(1)
    b = ClassicalRegister(1)
    circ = QuantumCircuit(q, b)

    # X nie działa w stanie superpozycji
    circ.x(q[0])
    circ.h(q[0])
    circ.x(q[0])
    circ.h(q[0])
    circ.measure(q[0], b[0])
    print(circ)

    job = execute(circ, backend=backend, shots=1024)
    st = job.result().get_counts()
    print(st)
