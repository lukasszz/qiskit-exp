from qiskit import Aer, QuantumRegister, ClassicalRegister, QuantumCircuit, execute

backend = Aer.get_backend('qasm_simulator')

q = QuantumRegister(5)
c = ClassicalRegister(5)

A, B, X, S, C = q

circ = QuantumCircuit()
circ.add_register(q)
circ.add_register(c)

circ.x(A)
circ.x(B)

circ.cx(A, S)
circ.cx(B, S)
circ.barrier()
circ.ccx(A, B, X)

circ.cx(X, C)
circ.cx(S, C)

circ.measure(q, c)
circ.ccx(X, S, C)

print(circ)

job = execute(circ, backend=backend, shots=1024)
st = job.result().get_counts()
if len(st) == 1:
    state = list(st.keys())[0][::-1]
    print("Input ABX=%s, result SC=%s " % (state[0:3], state[3:]))
else:
    print("Unexpected output")
    print(st)


