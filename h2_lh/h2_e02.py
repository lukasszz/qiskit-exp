# https://qiskit.org/documentation/aqua/chemistry/qiskit_chemistry_execution.html#execution-modes

from qiskit_chemistry import QiskitChemistry

distance = 0.735
molecule = 'H .0 .0 0; H .0 .0 {}'.format(distance)

# Input dictionaries to configure Qiskit Chemistry using QPE and Exact Eigensolver
qiskit_chemistry_qpe_dict = {
    'driver': {'name': 'PYSCF'},
    'PYSCF': {
        'atom': molecule,
        'basis': 'sto3g'
    },
    'operator': {'name': 'hamiltonian', 'transformation': 'full', 'qubit_mapping': 'bravyi_kitaev'},
    'algorithm': {
        'name': 'QPE',
        'num_ancillae': 9,
        'num_time_slices': 50,
        'expansion_mode': 'suzuki',
        'expansion_order': 2,
    },
    'initial_state': {'name': 'HartreeFock'},
    'backend': {
        'provider': 'qiskit.BasicAer',
        'name': 'qasm_simulator',
        'shots': 100,
    }
}

qiskit_chemistry_ees_dict = {
    'driver': {'name': 'PYSCF'},
    'PYSCF': {'atom': molecule, 'basis': 'sto3g'},
    'operator': {'name': 'hamiltonian', 'transformation': 'full', 'qubit_mapping': 'parity'},
    'algorithm': {
        'name': 'ExactEigensolver',
    },
}

# Execute the experiments
result_qpe = QiskitChemistry().run(qiskit_chemistry_qpe_dict, output='h2_e0_parity.txt')
#result_ees = QiskitChemistry().run(qiskit_chemistry_ees_dict)

# Extract the energy values
#print('The ground-truth ground-state energy is       {}.'.format(result_ees['energy']))
print('The ground-state energy as computed by QPE is {}.'.format(result_qpe['energy']))
#print('The Hartree-Fock ground-state energy is       {}.'.format(result_ees['hf_energy']))

