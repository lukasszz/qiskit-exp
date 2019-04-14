from qiskit_chemistry.drivers import PySCFDriver, UnitsType

'''
H_2 Hamilton integral with  1.43 UnitsType.BOHR = 0.7414 A
'''
driver = PySCFDriver(atom='H 0.0 0.0 0.0; H 0.0 0.0 1.41968', unit=UnitsType.BOHR,
                     charge=0, spin=0, basis='sto3g')
molecule = driver.run()

print(molecule.one_body_integrals)
print(molecule.two_body_integrals)

