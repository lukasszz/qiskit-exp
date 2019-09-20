from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram


def init_state(state, qc, qr):
    if '00' == state:
        pass
    elif '01' == state:
        qc.x(qr[0])
    elif '10' == state:
        qc.x(qr[1])
    elif '11' == state:
        qc.x(qr[0])
        qc.x(qr[1])


def circ_a(qc, qr):
    qc.h(qr[1])
    qc.cx(qr[0], qr[1])
    qc.h(qr[1])


def circ_b(qc, qr):
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.h(qr[0])


def circ_c(qc, qr):
    qc.h(qr[0])
    qc.h(qr[1])
    qc.cx(qr[0], qr[1])
    qc.h(qr[0])
    qc.h(qr[1])


if __name__ == '__main__':

    backend = Aer.get_backend('qasm_simulator')
    QR = QuantumRegister(2)
    CR = ClassicalRegister(2)

    states = ['00', '01', '10', '11']
    for s in states:
        QC = QuantumCircuit(QR, CR)
        init_state(s, QC, QR)
        circ_c(QC, QR)
        QC.measure(QR, CR)

        # print(QC.draw(output='text'))
        job = execute(QC, backend=backend, shots=1024)
        st = job.result().get_counts()
        print(s)
        print(st)
        # plot_histogram(st)
