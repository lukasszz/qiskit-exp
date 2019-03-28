import h5py
import numpy as np

# bash: $h5dump H2_equilibrium_0.735_sto-3g.hdf5 > H2_equilibrium_0.735_sto-3g.txt

# f = h5py.File('h2_0.735_sto-3g.hdf5', 'r')
f = h5py.File('H2_equilibrium_0.735_sto-3g.hdf5', 'r')

print(f.keys())
print('\n Orgin driver: ' + str(f.get('origin_driver').keys()))
print('\n Integrals: ' + str(f.get('integrals').keys()))
print('\n ==== mo_onee_ints ====\n' + str(np.array(f.get('integrals').get('mo_onee_ints'))))
print('\n ==== mo_eri_ints =====\n' + str(np.array(f.get('integrals').get('mo_eri_ints'))))

print('\n Geometry: ' + str(f.get('geometry').keys()))
print('\n ==== atom_xyz ====\n' + str(np.array(f.get('geometry').get('atom_xyz'))))
print('\n ==== multiplicity ====\n' + str(np.array(f.get('geometry').get('multiplicity'))))
print('\n ==== atom_symbol ====\n' + str(np.array(f.get('geometry').get('atom_symbol'))))
print('\n ==== molecular_charge ====\n' + str(np.array(f.get('geometry').get('molecular_charge'))))

# with h5py.File('h2_0.735_sto-3g.hdf5', 'r') as hf:
#     print('List of arrays in this file: \n', hf.keys())
#     data = hf.get('integrals')
#     print(data.keys())
#     #np_data = np.array(data)
    #print('Shape of the array dataset_1: \n', np_data.shape)

