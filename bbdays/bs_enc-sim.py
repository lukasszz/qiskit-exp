import time

import qiskit
from qiskit import IBMQ, QuantumRegister, ClassicalRegister, QuantumCircuit, compile, compiler, Aer
from qiskit.providers.jobstatus import JOB_FINAL_STATES
from qiskit.visualization import plot_histogram

qiskit.IBMQ.load_accounts()
# backend = IBMQ.backends(name='ibmq_ourense')[0]
#backend = IBMQ.backends(name='ibmq_16_melbourne')[0]
backend = Aer.get_backend('qasm_simulator')

q3 = QuantumRegister(3)
c3 = ClassicalRegister(3)
circ = QuantumCircuit(q3, c3)

alpha = .5
circ.initialize([.0, alpha, alpha, .0, alpha, .0, .0, alpha], q3)
circ.measure(q3, c3)
# print(circ)

circ = compiler.transpile(circ, backend)
qobj = compiler.assemble(circ, backend, shots=1024)

job = backend.run(qobj)

start_time = time.time()
job_status = job.status()
while job_status not in JOB_FINAL_STATES:
    print(f'Status @ {time.time()-start_time:0.0f} s: {job_status.name},'
          f' est. queue position: ')
    time.sleep(10)
    job_status = job.status()

result = job.result()
print(result.get_counts())


plot_histogram(result.get_counts())
