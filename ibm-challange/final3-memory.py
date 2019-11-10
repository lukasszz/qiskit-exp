from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

""" 


"""
mem_input = QuantumRegister(1)  # input
mem_ancilla = QuantumRegister(1)  # anclia
mem_output = QuantumRegister(1)  # output

c = ClassicalRegister(1)

circ = QuantumCircuit()
circ.add_register(mem_input)
circ.add_register(mem_ancilla)
circ.add_register(c)
circ.add_register(mem_output)


def mem():
    circ.barrier()
    # cmp_res OR previous_output > ancila
    circ.cx(mem_input, mem_ancilla)
    circ.cx(mem_output, mem_ancilla)
    circ.ccx(mem_input, mem_output, mem_ancilla)

    # move ancila (OR result) output and clean ancila
    circ.swap(mem_ancilla, mem_output)
    circ.reset(mem_ancilla)


if __name__ == '__main__':

    # input 1

    # inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # inputs = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    # inputs = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # inputs = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    # inputs = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    # inputs = [1, 1, 1, 1, 1, 1, 1]
    # inputs = [1, 0, 1, 1, 1, 1, 1]
    # inputs = [0, 1, 1, 1, 1, 1, 1]
    # inputs = [1, 1, 1, 1, 1, 1, 0]
    # inputs = [1, 0, 1, 1, 1, 1, 0]
    inputs = [1, 0, 1, 1, 0, 1, 1]
    # inputs = [1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
    for i1 in inputs:
        if 1 == i1:
            circ.x(mem_input)
        mem()
        # circ.barrier()

    circ.measure(mem_output, c)

    # run
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend=backend, shots=1024)

    print(circ.draw(line_length=200))
    print(job.result().get_counts())
