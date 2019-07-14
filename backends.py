import pickle
from datetime import datetime

import qiskit
from qiskit import IBMQ
from qiskit.providers.models import BackendStatus

qiskit.IBMQ.load_accounts()
# backends = Aer.backends()
backends = IBMQ.backends()

backends_status = []
for b in backends:
    print(b.name() + " status: ", end='')
    print(b.status())
    st: BackendStatus = b.status()
    backends_status.append({'pendging_jobs': st.pending_jobs,
                            'name': st.backend_name,
                            'operational': st.operational})

print("Dump to file")
data = {'tms': datetime.utcnow(), 'backends': backends_status}
f = open('ibm_backends.pickle', 'wb')
pickle.dump(data, f)
f.close()

print("Load form file")
f = open('ibm_backends.pickle', 'rb')
dr = pickle.load(f)
print(dr['tms'])
print(dr['backends'])
