"""
https://github.com/quantum-challenge/2019/blob/master/problems/week1/week1_en.ipynb
"""
import json

from qiskit import Aer, QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller

backend = Aer.get_backend('qasm_simulator')


class FullAdder:
    """
    Input:
    A input
    B input
    X carry in

    Reuslt:
    S sum
    C carry out
    """

    def __init__(self):
        self.q = QuantumRegister(6)
        self.c = ClassicalRegister(6)
        self.circ = QuantumCircuit()
        self.circ.add_register(self.q)
        self.circ.add_register(self.c)
        # c1s1 is the register for half adder summation - for the AB bits
        self.A, self.B, self.X, self.c1, self.S, self.C = self.q
        self.result_state = []
        self.result = {'ABX': '00', 'c1': '0', 'CS': '00'}

        self.q2 = QuantumRegister(6)
        self.circ.add_register(q2)
        self.A2, self.B2, self.X2, self.c12, self.S2, self.C2 = self.q2

    def build_circ(self):
        self.circ.cx(self.A, self.S)
        self.circ.cx(self.B, self.S)
        self.circ.cx(self.X, self.S)
        self.circ.ccx(self.A, self.B, self.c1)
        self.circ.barrier()

        self.circ.cx(self.X, self.C)
        self.circ.cx(self.c1, self.C)
        self.circ.ccx(self.X, self.S, self.C)
        self.circ.barrier()


    def build_circ2(self):
        self.circ.cx(self.S, self.S2)
        self.circ.cx(self.C, self.S2)
        self.circ.cx(self.X, self.S)
        self.circ.ccx(self.A, self.B, self.c1)
        self.circ.barrier()

        self.circ.cx(self.X, self.C)
        self.circ.cx(self.c1, self.C)
        self.circ.ccx(self.X, self.S, self.C)
        self.circ.barrier()

    def input(self, abx):
        if '1' == abx[0]:
            self.circ.x(self.A)
        if '1' == abx[1]:
            self.circ.x(self.B)
        if '1' == abx[2]:
            self.circ.x(self.X)

        self.circ.barrier()

    def run(self):
        self.circ.measure(self.q, self.c)
        job = execute(self.circ, backend=backend, shots=1024)
        st = job.result().get_counts()
        if len(st) == 1:
            # self.result_state = list(st.keys())[0][::-1]
            self.result_state = list(st.keys())[0]
            self.result['ABX'] = self.result_state[3:6][::-1]
            self.result['c1'] = self.result_state[2:3]
            self.result['CS'] = self.result_state[0:2]
        else:
            print("Unexpected output")
            print(st)

    def print_result_state(self):
        print(self.result_state)
        print("Input ABX=%s, c1=%s result CS=%s " % (self.result['ABX'], self.result['c1'], self.result['CS']))


def test(abx, cs):
    fa = FullAdder()
    fa.input(abx)
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()
    assert cs == fa.result['CS']
    return fa.result['CS']


def carry_loop():
    fa.circ.cx(fa.C, fa.X)
    fa.circ.cx(fa.S, fa.X)
    fa.circ.ccx(fa.S, fa.C, fa.X)


if '__main__' == __name__:

    fa = FullAdder()

    # set A to 1
    fa.circ.x(fa.A)
    fa.build_circ()

    #+0
    fa.circ.x(fa.A)
    fa.build_circ()

    #+0
    fa.circ.x(fa.A)
    fa.build_circ()

    # # A is again 1
    # carry_loop()
    # fa.build_circ()
    #
    # # A is again 1
    # carry_loop()
    # fa.build_circ()


    fa.run()
    print(fa.circ.draw(line_length=200))
    fa.print_result_state()
