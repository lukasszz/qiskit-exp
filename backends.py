import qiskit

qiskit.IBMQ.load_accounts()
backends = qiskit.IBMQ.backends()
for b in backends:
    print(b.name() + " status: ", end='')
    print(b.status())
