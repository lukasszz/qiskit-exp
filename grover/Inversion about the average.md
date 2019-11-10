# Inversion about the average

**Q1: It is the special superposition-entaglement state. It is not the same as usage only of the H + CNOT?**

It is not creating the superposition. The superposition of the system is created on the very beginning with the H gates acting on every qubit.  The reflection (inversion?) about the average is for multiplying the amplitude of searched item and lowering the others.



**Q2: How ancilla qubit affects the operating qubits? It looks like the operting qubits only controll the state of ancilla.**

The ccz gate (entagle?) the qubits.

Changes in ancilla qubits also affetcs the controlled qubits according to phase kickback.

https://www.quora.com/What-is-phase-kickback-and-how-does-it-occur

## How to act on a single qubit in qubyte?

`/home/lukasz/workspace/qiskit-exp/ibm-challange/Inversion about the avarage.ipynb`

I wonder how to do matrix computation using numpy doing the quantum gates on the QuantumRegister.
$$
|0> |0> 
H|0> |0>
|+> |0> = 1/\sqrt(2))|0> + 1/\sqrt(2)|1> |0>
$$




How to manipulate (in matrix fashion) on a single qubit after entanglement (two qubit gate)?

circ.h(q[0])
circ.cx(q[0], q[1])

How to do that in numpy?

circ.x(q[1])

We need to multiple the X with the I matrix.

Introduction to Quantum Circuits > States for many qubits

https://quantum-computing.ibm.com/support/guides/introduction-to-quantum-circuits?page=5cae6f5c35dafb4c01214bbd



That works. Comparing with `qiskit ` results we need to have into memory the little ednian notation.

So now, I need to know how to do the CX10. https://arxiv.org/pdf/0705.4171.pdf



Groover steps:

https://quantum-computing.ibm.com/support/guides/quantum-algorithms-with-qiskit?page=5cc0d9fd86b50d00642353ca#amplitude-amplification

1. We don't know which item. It could be any of them - so every is in the supperpostion. Applay H to every qubit. (The uniform superposition is easily constructed from |s⟩=H⊗n|0⟩n|s⟩=H⊗n|0⟩n)

   1. Enter the procedure
   2. Apply the Oracle (the marked state has minus amplitude - TODO: check histogram)
   3. apply H
   4. Apply the reflection about the avarge
   5. apply H
   6. contiune loop or measure

   (prepare ) H > (loop) Oracle > H > reflection about avarage > H > (loop/measure)

## Questions

1. Why for the Groover algo we need to prepare the inversion_about_avarage, and not to do a simple h+cx enteltagment? Are this two states different?

2. ```python
   # |10> ?? Works but don't know why this oracle amplifiy te 01-state
   ```

   