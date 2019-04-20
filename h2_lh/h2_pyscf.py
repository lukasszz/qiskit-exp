from pyscf import gto, scf, ao2mo
import numpy as np

mol = gto.M(atom='H 0 0 0; H 0 0 0.7414', basis='sto3g')
mol.build()
mf = scf.RHF(mol)
ehf = mf.kernel()

hij = mf.get_hcore()
print(hij)
print("Mo coeff: " + str(mf.mo_coeff))
mohij = np.dot(np.dot(mf.mo_coeff.T, hij), mf.mo_coeff)
print(mohij)

print("Orbitals energies %s" % mf.mo_energy)

mf.get_ovlp()
mf.get_jk()
mf.get_k()

# norbs = mo_coeff.shape[0]
# eri = ao2mo.incore.full(mf._eri, mo_coeff, compact=False)
# mohijkl = eri.reshape(norbs, norbs, norbs, norbs)

#enuke = gto.mole.energy_nuc(mol) # Nuclear repulsion energy
#print(enuke)

