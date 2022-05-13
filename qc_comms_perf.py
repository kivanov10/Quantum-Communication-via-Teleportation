import qiskit as q
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector
from qiskit.result import marginal_counts
import numpy as np
import matplotlib.pyplot as plt

#tamper with the wavefunction on purpouse
class qc_comms:
    def __init__(self):
        self.random_state()
        self.init_circuit()
        plot_bloch_multivector(self.psi)
        #Add the random statevector to the qc
        self.qc.append(self.init_gate, [0])
        self.qc.barrier()

        #Third party makes a entagled pair and gives one to sender and one to
        #receiver
        self.bell_pair(self.qc, 1, 2)
        self.qc.barrier()

        self.sender_gates(0, 1)

        #Sender sends classical bits to receiver
        self.measure_and_send(self.qc, 0, 1)

        #Receiver decodes his qubit
        self.receiver_gates(self.qc, 2, self.bits_z, self.bits_x)

        self.qc.draw('mpl')
        # plt.show()
        self.sim = q.Aer.get_backend('aer_simulator')
        self.qc.save_statevector()
        out_vector = self.sim.run(self.qc).result().get_statevector()
        plot_bloch_multivector(out_vector)
        # plt.show()
        # Error is here, disentagler is not recognised by line 47
        # self.qc.append(self.init_gate_inv, [2])
        self.qc.measure(2,2)
        self.qc.draw('mpl')
        # print(self.qc)
        # big_qc = q.transpile(self.qc, self.sim)
        # big_qc.save_statevector()
        # print(big_qc)
        # results = self.sim.run(self.qc).result().get_counts()
        # qubit_counts = [marginal_counts(results, [qub]) for qub in range(3)]
        # plot_histogram(qubit_counts)
        print('lol')
        plt.show()


    def random_state(self):
        """Creates a random statevector it's inverse"""
        self.psi = random_statevector(2)
        self.init_gate = Initialize(self.psi)
        self.init_gate_inv = self.init_gate.gates_to_uncompute()
        self.init_gate.label = "Random state"


    def init_circuit(self):
        """Initializes the quantum circuit"""
        qubits = q.QuantumRegister(3, name='qbit')
        self.bits_z = q.ClassicalRegister(1, name='bit_z')
        self.bits_x = q.ClassicalRegister(1, name='bit_x')
        self.bits_r = q.ClassicalRegister(1, name='bit_rec')
        self.qc = q.QuantumCircuit(qubits, self.bits_z, self.bits_x, self.bits_r)

    def bell_pair(self, qc, q1, q2):
        """Creates a bell pair with q1 being control. These qubits are then "sent"
        to the two people the protocol will be working with
        """
        self.qc.h(q1) #Hadamard
        self.qc.cx(q1,q2) #CNOT


    def measure_and_send(self,qc,q1,q2):
        """Measures qubits a & b and 'sends' the results to Bob"""
        self.qc.barrier()
        self.qc.measure(q1,0)
        self.qc.measure(q2,1)

    def sender_gates(self,psi,q1):
        """Sender instructions"""
        self.qc.cx(psi,q1)
        self.qc.h(psi)

    def receiver_gates(self,qc,qbits,bit_z,bit_x):
        # Here we use c_if to control our gates with a classical
        # bit instead of a qubit
        self.qc.x(qbits).c_if(bit_x, 1) # Apply gates if the registers
        self.qc.z(qbits).c_if(bit_z, 1) # are in the state '1'

qc = qc_comms()
