from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

""" 
"""

q = QuantumRegister(10)
c = ClassicalRegister(10)
an = QuantumRegister(1)
s = QuantumRegister(1)
sc = ClassicalRegister(1)
circ = QuantumCircuit()
circ.add_register(q)
circ.add_register(an)
circ.add_register(s)
circ.add_register(c)
circ.add_register(sc)


def init_map():
    # A: 00 red
    # B: 01 blue
    # C: 10 yellow
    # D: 11 green

    # 1 D
    circ.x(q[0])
    circ.x(q[1])

    # 2 A
    # q[2]
    # q[3]

    # 3 B
    # q[4]
    circ.x(q[5])

    # 4 D
    circ.x(q[6])
    circ.x(q[7])

    # 5 A
    # q[8]
    # q[9]


def cmp(a, b):
    # compare into the second vertice
    circ.cx(a[0], b[0])
    circ.cx(a[1], b[1])
    circ.cx(b[0], an)
    circ.cx(b[1], an)
    circ.ccx(b[0], b[1], an)# q[4] = 0 the same BAD , 1 odd OK
    # OR if there was at least one adjenct
    circ.x(an)
    circ.cx(an, s)  # q[5] - if there were at least one the same adjenct chains q5 will by 1

    # revert scecond vertice
    circ.cx(a[1], b[1])
    circ.cx(a[0], b[0])

    circ.reset(an)


def run():
    circ.measure(s, sc)
    circ.measure(q, c)
    # run
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    print(job.result().get_counts())


if __name__ == '__main__':
    init_map()
    cmp((q[0], q[1]), (q[2], q[3]))  # 1 - 2
    cmp((q[0], q[1]), (q[4], q[5]))  # 1 - 3
    cmp((q[0], q[1]), (q[8], q[9]))  # 1 - 5
    cmp((q[2], q[3]), (q[4], q[5]))  # 2 - 3
    cmp((q[2], q[3]), (q[6], q[7]))  # 2 - 4
    cmp((q[4], q[5]), (q[6], q[7]))  # 3 - 4
    cmp((q[4], q[5]), (q[8], q[9]))  # 3 - 5
    cmp((q[6], q[7]), (q[8], q[9]))  # 4 - 5

    cmp((q[2], q[3]), (q[8], q[9]))  # 2 - 5 (adjacent)
    cmp((q[0], q[1]), (q[6], q[7]))  # 1 - 4 (adjacent)


    run()
