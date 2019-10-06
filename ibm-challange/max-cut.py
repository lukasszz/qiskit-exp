from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

""" 
vertices:   (q0)---(q1)---(q2)
                 |      |
ce_checker:      q3     q4

sum cuts:    q5 - carry out 
             q6 - sum
oracle:      q7
                
"""
q = QuantumRegister(8)
c = ClassicalRegister(8)
circ = QuantumCircuit()
circ.add_register(q)
circ.add_register(c)


def prepare_v1():
    """ Put vertices in the zones. Into the superposition state to check all the possibilites once.
    """
    circ.h(q[0:3])


def prepare_v2():
    """ Put vertices in the zones. Into the superposition state to check all the possibilites once.
    """
    circ.h(q[0:3])

    # Oracle phase flip
    circ.x(q[7])
    circ.h(q[7])


def cutter_edge_checker(a: QuantumRegister, b: QuantumRegister, res: QuantumRegister):
    """ Checks if two connected vertices are:
        - in the same zone   (00, 11)->(0) or
        - in different zones (01, 10)->(1)
                             (ab)->res

    """
    circ.cx(a, res)
    circ.cx(b, res)


def count_cuts():
    """ Counts how many cuts do we have by making the summation of the ce_checkers.
        It is done by the half adder
    """
    circ.cx(q[3], q[6])
    circ.cx(q[4], q[6])
    circ.ccx(q[3], q[4], q[5])


def oracle():
    """ Oracle is for finding the cuts grater than 2.
        So it checks if carry out (q6) from the half adder is 1
    """
    circ.cx(q[5], q[7])


def oracle_v2():
    """ Oracle is for finding the cuts grater than 2.
        So it checks if carry out (q6) from the half adder is 1
    """
    circ.cz(q[5], q[7])


def run():
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)
    return job.result()


def max_cut_test_oracle():
    prepare_v1()
    cutter_edge_checker(q[0], q[1], q[3])
    cutter_edge_checker(q[1], q[2], q[4])
    count_cuts()
    oracle()
    circ.measure(q[7], c[7])
    res = run()
    # {'10000000': 258, '00000000': 766}
    # There are 8 possible states for 3 qubits. We know 101 and 010 are the states with max cut.
    # Our oracle meausred that 766 there are les then 2 cuts and 258 times there were more then 2 cuts
    # It seams that the oracle properly works. But we still didn't determined this states from the program.
    print("max_cut_v1 (to the Oracle)")
    print(res.get_counts())
    # print(circ)


def clean_helper_registers():
    """ We need to clean helper registers count cut, and half adder so they dont have an input for the final result.
        (to eliminate unnecessary entanglements between the input qubits)
        We do that by inversing this part of circuit
    """

    # invert half adder
    circ.ccx(q[3], q[4], q[5])
    circ.cx(q[4], q[6])
    circ.cx(q[3], q[6])
    # invert counting edges
    #     cutter_edge_checker(q[1], q[2], q[4])
    circ.cx(q[2], q[4])
    circ.cx(q[1], q[4])
    #     cutter_edge_checker(q[0], q[1], q[3])
    circ.cx(q[1], q[3])
    circ.cx(q[0], q[3])


def amplitude_amplification(a, b, c):
    """
        diffusion operations
    """
    circ.h(q[a])
    circ.h(q[b])
    circ.h(q[c])
    circ.x(q[a])
    circ.x(q[b])
    circ.x(q[c])
    circ.h(q[c])
    circ.ccx(q[a], q[b], q[c])
    circ.h(q[c])
    circ.x(q[a])
    circ.x(q[b])
    circ.x(q[c])
    circ.h(q[a])
    circ.h(q[b])
    circ.h(q[c])


def max_cut_v2_find_solution():
    prepare_v2()
    circ.barrier()

    # Oracle part
    cutter_edge_checker(q[0], q[1], q[3])
    cutter_edge_checker(q[1], q[2], q[4])
    count_cuts()
    oracle_v2()
    circ.barrier()

    clean_helper_registers()
    circ.barrier()

    amplitude_amplification(0, 1, 2)
    circ.barrier()

    circ.measure(q[0:3], c[0:3])
    res = run()

    print("max_cut_v2 (Oracle phase flip)")
    print(circ.draw(output='text', line_length=200))
    print(res.get_counts())
    print("We have found the answear: '00000101': high, '00000010': high,")


if __name__ == '__main__':
    # max_cut_test_oracle()
    # or
    max_cut_v2_find_solution()
