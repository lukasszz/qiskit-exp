"""
This experiment computes the H2 molecule energy starting from provided HDF5 file
First with Exect method then o the quantum simulator.

https://nbviewer.jupyter.org/github/Qiskit/qiskit-tutorial/blob/master/qiskit/aqua/chemistry/dissociation_profile_of_molecule.ipynb

"""
from qiskit import Aer
from qiskit_chemistry import QiskitChemistry

qiskit_chemistry_dict = {
    'driver': {'name': 'HDF5'},
    'HDF5': {'hdf5_input': 'H2_equilibrium_0.735_sto-3g.hdf5'},
    'operator': {'name': 'hamiltonian',
                 'qubit_mapping': 'parity',
                 'two_qubit_reduction': True},
    'algorithm': {'name': 'ExactEigensolver'}
}
solver = QiskitChemistry()
result = solver.run(qiskit_chemistry_dict)
print('Ground state energy (classical): {:.12f}'.format(result['energy']))

# Second, we use variational quantum eigensolver (VQE)
qiskit_chemistry_dict['algorithm']['name'] = 'VQE'
qiskit_chemistry_dict['optimizer'] = {'name': 'SPSA', 'max_trials': 350}
qiskit_chemistry_dict['variational_form'] = {'name': 'RYRZ', 'depth': 3, 'entanglement': 'full'}
backend = Aer.get_backend('statevector_simulator')

solver = QiskitChemistry()
result = solver.run(qiskit_chemistry_dict, backend=backend)
print('Ground state energy (quantum)  : {:.12f}'.format(result['energy']))
print("====================================================")
# You can also print out other info in the field 'printable'
for line in result['printable']:
    print(line)
