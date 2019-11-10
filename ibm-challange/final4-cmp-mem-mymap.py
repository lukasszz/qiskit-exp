from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

""" 
"""

q = QuantumRegister(12)
c = ClassicalRegister(12)
cmp_ancilla = QuantumRegister(1)
cmp_res = QuantumRegister(1)
sc = ClassicalRegister(1)
circ = QuantumCircuit()
circ.add_register(q)
circ.add_register(cmp_ancilla)
circ.add_register(cmp_res)
circ.add_register(c)
circ.add_register(sc)

mem_ancilla = QuantumRegister(1)  # anclia
mem_output = QuantumRegister(1)  # output
mem_output_c = ClassicalRegister(1)
circ.add_register(mem_ancilla, mem_output, mem_output_c)


def mem(mem_input):
    circ.barrier()
    # cmp_res OR previous_output > ancila
    circ.cx(mem_input, mem_ancilla)
    circ.cx(mem_output, mem_ancilla)
    circ.ccx(mem_input, mem_output, mem_ancilla)

    # move ancila (OR result) output and clean ancila
    circ.swap(mem_ancilla, mem_output)
    circ.reset(mem_ancilla)


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

    # 6 C
    circ.x(q[10])
    # q[11]


def cmp(a, b):
    # compare into the second vertice
    circ.cx(a[0], b[0])
    circ.cx(a[1], b[1])
    circ.cx(b[0], cmp_ancilla)
    circ.cx(b[1], cmp_ancilla)
    circ.ccx(b[0], b[1], cmp_ancilla)  # q[4] = 0 the same BAD , 1 odd OK
    # OR if there was at least one adjenct
    circ.x(cmp_ancilla)
    circ.cx(cmp_ancilla, cmp_res)  # q[5] - if there were at least one the same adjenct chains q5 will by 1

    # revert scecond vertice
    circ.cx(a[1], b[1])
    circ.cx(a[0], b[0])

    circ.reset(cmp_ancilla)


def run():
    circ.measure(cmp_res, sc)
    circ.measure(q, c)
    circ.measure(mem_output, mem_output_c)
    # run
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    print(job.result().get_counts())


if __name__ == '__main__':
    init_map()
    cmp((q[0], q[1]), (q[2], q[3]))  # 1 - 2
    mem(cmp_res)
    cmp((q[0], q[1]), (q[4], q[5]))  # 1 - 3
    mem(cmp_res)
    cmp((q[0], q[1]), (q[8], q[9]))  # 1 - 5
    mem(cmp_res)
    cmp((q[2], q[3]), (q[4], q[5]))  # 2 - 3
    mem(cmp_res)
    cmp((q[2], q[3]), (q[6], q[7]))  # 2 - 4
    mem(cmp_res)
    cmp((q[4], q[5]), (q[6], q[7]))  # 3 - 4
    mem(cmp_res)
    cmp((q[4], q[5]), (q[8], q[9]))  # 3 - 5
    mem(cmp_res)
    cmp((q[6], q[7]), (q[8], q[9]))  # 4 - 5
    mem(cmp_res)
    cmp((q[2], q[3]), (q[10], q[11]))  # 2 - 6
    mem(cmp_res)

    # test modification with adjacent
    # # 1
    # cmp((q[2], q[3]), (q[8], q[9]))  # 2 - 5 (adjacent)
    # mem(cmp_res)
    # # 2
    # cmp((q[0], q[1]), (q[6], q[7]))  # 1 - 4 (adjacent)
    # mem(cmp_res)

    # # 3
    # cmp((q[2], q[3]), (q[8], q[9]))  # 2 - 5 (adjacent)
    # mem(cmp_res)
    # cmp((q[0], q[1]), (q[6], q[7]))  # 1 - 4 (adjacent)
    # mem(cmp_res)

    run()
