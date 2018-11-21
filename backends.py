import pickle
from datetime import datetime

import qiskit

qiskit.IBMQ.load_accounts()
backends = qiskit.IBMQ.backends()
backends_status = []
for b in backends:
    print(b.name() + " status: ", end='')
    print(b.status())
    backends_status.append(b.status())

# Dump to file
data = {'tms': datetime.utcnow(), 'backends': backends_status}
f = open('ibm_backends.pickle', 'wb')
pickle.dump(data, f)
f.close()

# Load form file
f = open('ibm_backends.pickle', 'rb')
dr = pickle.load(f)
print(dr['tms'])
print(dr['backends'])
