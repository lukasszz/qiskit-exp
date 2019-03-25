# import common packages
import numpy as np

from qiskit import Aer

# lib from Qiskit Aqua
from qiskit_aqua import Operator, QuantumInstance
from qiskit_aqua.algorithms import VQE, ExactEigensolver
from qiskit_aqua.components.optimizers import COBYLA

# lib from Qiskit Aqua Chemistry
from qiskit_chemistry import FermionicOperator
from qiskit_chemistry.drivers import PySCFDriver, UnitsType
from qiskit_chemistry.aqua_extensions.components.variational_forms import UCCSD
from qiskit_chemistry.aqua_extensions.components.initial_states import HartreeFock


# using driver to get fermionic Hamiltonian
# PySCF example
driver = PySCFDriver(atom='H 0.0 0.0 0.0; H 0.0 0.0 0.735', unit=UnitsType.ANGSTROM,
                     charge=0, spin=0, basis='sto3g')
molecule = driver.run()

# please be aware that the idx here with respective to original idx
freeze_list = [0]
remove_list = [-3, -2] # negative number denotes the reverse order
map_type = 'parity'
map_type = 'bksf'
#map_type = 'bravyi_kitaev'

h1 = molecule.one_body_integrals
h2 = molecule.two_body_integrals
nuclear_repulsion_energy = molecule.nuclear_repulsion_energy

num_particles = molecule.num_alpha + molecule.num_beta
num_spin_orbitals = molecule.num_orbitals * 2
print("HF energy: {}".format(molecule.hf_energy - molecule.nuclear_repulsion_energy))
print("# of electrons: {}".format(num_particles))
print("# of spin orbitals: {}".format(num_spin_orbitals))

# prepare full idx of freeze_list and remove_list
# convert all negative idx to positive
remove_list = [x % molecule.num_orbitals for x in remove_list]
freeze_list = [x % molecule.num_orbitals for x in freeze_list]
# update the idx in remove_list of the idx after frozen, since the idx of orbitals are changed after freezing
remove_list = [x - len(freeze_list) for x in remove_list]
remove_list += [x + molecule.num_orbitals - len(freeze_list)  for x in remove_list]
freeze_list += [x + molecule.num_orbitals for x in freeze_list]

# prepare fermionic hamiltonian with orbital freezing and eliminating, and then map to qubit hamiltonian
# and if PARITY mapping is selected, reduction qubits
energy_shift = 0.0
qubit_reduction = True if map_type == 'parity' else False

ferOp = FermionicOperator(h1=h1, h2=h2)
# if len(freeze_list) > 0:
#     ferOp, energy_shift = ferOp.fermion_mode_freezing(freeze_list)
#     num_spin_orbitals -= len(freeze_list)
#     num_particles -= len(freeze_list)
# if len(remove_list) > 0:
#     ferOp = ferOp.fermion_mode_elimination(remove_list)
#     num_spin_orbitals -= len(remove_list)

qubitOp = ferOp.mapping(map_type=map_type, threshold=0.00000001)
qubitOp = qubitOp.two_qubit_reduced_operator(num_particles) if qubit_reduction else qubitOp
qubitOp.chop(10**-10)

print(qubitOp.print_operators())
print(qubitOp)

exact_eigensolver = ExactEigensolver(qubitOp, k=1)
ret = exact_eigensolver.run()
print('The computed energy is: {:.12f}'.format(ret['eigvals'][0].real))
print('The total ground state energy is: {:.12f}'.format(ret['eigvals'][0].real + energy_shift + nuclear_repulsion_energy))


# Bravyi-Kitaev Superfast simulation of electronic structure on a quantum computer
# Kanav Setia 1 and James D. Whitfield

# H BKSF = − 0.045321σ 4 z σ 3 x σ 2 x σ 1 z − 0.045321σ 4 z σ 3 y σ 2 y σ 1 z
# + 0.171201σ 2 z σ 1 z + 0.045321σ 4 x σ 1 x
# + 0.171201σ 3 z σ 1 z + 0.3429725σ 3 z σ 2 z
# + 0.045321σ 4 y σ 1 y − 0.2227965σ 4 z σ 3 z
# + 0.045321σ 4 y σ 3 z σ 2 z σ 1 y − 0.2227965σ 4 z σ 2 z
# − 0.045321σ 3 y σ 2 y + 0.2410925σ 4 z σ 3 z σ 2 z σ 1 z
# + 0.331736σ 4 z σ 1 z − 0.812610I
# (47)