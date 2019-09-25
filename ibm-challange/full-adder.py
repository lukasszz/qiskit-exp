"""
https://github.com/quantum-challenge/2019/blob/master/problems/week1/week1_en.ipynb
"""
from qiskit import Aer, QuantumRegister, ClassicalRegister, QuantumCircuit, execute

backend = Aer.get_backend('qasm_simulator')


class FullAdder():

    def __init__(self):
        self.q = QuantumRegister(7)
        self.c = ClassicalRegister(7)
        self.circ = QuantumCircuit()
        self.circ.add_register(self.q)
        self.circ.add_register(self.c)
        self.A, self.B, self.X, self.s1, self.c1, self.S, self.C = self.q
        self.result_state = []

    def build_circ(self):
        self.circ.cx(self.A, self.s1)
        self.circ.cx(self.B, self.s1)
        self.circ.ccx(self.A, self.B, self.c1)
        self.circ.barrier()

        self.circ.cx(self.X, self.S)
        self.circ.cx(self.S, self.C)

        self.circ.measure(self.q, self.c)
        self.circ.ccx(self.X, self.S, self.C)

    def input(self, abx):
        if '1' == abx[0]:
            self.circ.x(self.A)
        if '1' == abx[1]:
            self.circ.x(self.B)
        if '1' == abx[2]:
            self.circ.x(self.X)

        self.circ.barrier()

    def run(self):
        job = execute(self.circ, backend=backend, shots=1024)
        st = job.result().get_counts()
        if len(st) == 1:
            # self.result_state = list(st.keys())[0][::-1]
            self.result_state = list(st.keys())[0]
        else:
            print("Unexpected output")
            print(st)

    def print_result_state(self):
        print("Input XBA=%s, s1c1=%s result SC=%s " % (self.result_state[4:7], self.result_state[2:4], self.result_state[0:2]))


# print(circ)


if '__main__' == __name__:
    print('abc')
    fa = FullAdder()
    fa.input('100')
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()

    fa = FullAdder()
    fa.input('110')
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()

    fa = FullAdder()
    fa.input('000')
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()

    fa = FullAdder()
    fa.input('010')
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()

    fa = FullAdder()
    fa.input('001')
    fa.build_circ()
    # print(fa.circ)
    fa.run()
    fa.print_result_state()
