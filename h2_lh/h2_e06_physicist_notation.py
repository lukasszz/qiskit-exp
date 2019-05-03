"""
qiskit_chemistry.fermionic_operator.FermionicOperator#__init__
If you are using the 'physicist' notation, you need to convert it to
the 'chemist' notation first. E.g., h2 = numpy.einsum('ikmj->ijkm', h2)
"""

import numpy as np
from qiskit_chemistry import FermionicOperator
from qiskit_chemistry.drivers import PySCFDriver, UnitsType

driver = PySCFDriver(atom='H 0.0 0.0 0.0; H 0.0 0.0 1.41968', unit=UnitsType.BOHR,
                     charge=0, spin=0, basis='sto3g')
molecule = driver.run()

h2 = molecule.two_body_integrals

h2p = np.einsum('ijkm->ikmj', h2)
print("########## Chemist notation #########")
print(h2)
print("########## Physicist notation #########")
print(h2p)

# ferOp = FermionicOperator(h1=molecule.one_body_integrals, h2=molecule.two_body_integrals)
