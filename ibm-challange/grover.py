import json

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller


def inversion_about_average(circ, qr):
    """Apply inversion about the average step of Grover's algorithm."""

    circ.h(qr[0:2])
    circ.x(qr[0:2])

    # circ.h(qr[1])
    # circ.cx(qr[0], qr[1])
    # circ.h(qr[1])
    # it's just cz
    circ.cz(qr[0], qr[1])

    circ.x(qr[0:2])
    circ.h(qr[0:2])


def inversion_about_average2(circ, qr):
    """Apply inversion about the average step of Grover's algorithm."""

    circ.h(qr)

    circ.cx(qr[0], qr[1])
    # circ.x(qr)
    # circ.h(qr)


def grover11_ancilla():
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    circ = QuantumCircuit()
    circ.add_register(q)
    circ.add_register(c)


    circ.x(q[2]) # X on ancilla qbit

    # H
    circ.h(q[0:2])

    # Oracle

    circ.x(q[0])
    circ.h(q[2])
    circ.ccx(q[0], q[1], q[2])
    circ.h(q[2])
    inversion_about_average(circ, q)

    circ.measure(q, c)
    # print(circ)
    return circ


def grover11():
    q = QuantumRegister(2)
    c = ClassicalRegister(2)
    circ = QuantumCircuit()
    circ.add_register(q)
    circ.add_register(c)

    circ.h(q)
    circ.cz(q[0], q[1])

    inversion_about_average(circ, q)

    circ.measure(q, c)
    return circ


def grover10_ancilla():
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    circ = QuantumCircuit()
    circ.add_register(q)
    circ.add_register(c)


    circ.x(q[2]) # X on ancilla qbit

    # H
    circ.h(q[0:2])

    # Oracle from example
    # circ.h(q[2])
    # circ.x(q[0])
    # circ.ccx(q[0], q[1], q[2])
    # circ.x(q[0])
    # circ.h(q[2])

    # My Oracle
    circ.h(q[2])
    circ.z(q[1])
    circ.ccx(q[0], q[1], q[2])
    circ.h(q[2])

    inversion_about_average(circ, q)

    circ.measure(q, c)
    # print(circ)
    return circ


def grover10():
    q = QuantumRegister(2)
    c = ClassicalRegister(2)
    circ = QuantumCircuit()
    circ.add_register(q)
    circ.add_register(c)

    # H
    circ.h(q)

    # Oracle
    circ.cz(q[0], q[1])
    circ.x(q[0])

    inversion_about_average(circ, q)

    circ.measure(q, c)
    return circ


def run_circ():
    print("Groover 11")
    circ = grover11()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    st = job.result().get_counts()
    print(st)

    print("Groover 10")
    circ = grover10()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    st = job.result().get_counts()
    print(st)


    print("Groover 11 ancilla")
    circ = grover11_ancilla()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    st = job.result().get_counts()
    print(st)

    print("Groover 10 ancilla")
    circ = grover10_ancilla()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    st = job.result().get_counts()
    print(st)

    # now let's check the quantum cost of this circuit by using the Unroller.
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(circ)
    # print(new_circuit)
    print(new_circuit.count_ops())
    with open('wk2_output-last-run.txt', 'w') as f:
        f.write(json.dumps(new_circuit.count_ops()))

    # plot_histogram(st)


if '__main__' == __name__:
    run_circ()
