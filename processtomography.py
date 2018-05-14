import matplotlib.pyplot as plt
from grove.tomography.process_tomography import do_process_tomography
from pyquil.api import CompilerConnection
from pyquil.api import QVMConnection
from pyquil.api import get_devices
from pyquil.gates import *
from pyquil.quil import Program

qvm = QVMConnection()
acorn = get_devices(as_dict=True)['19Q-Acorn']

# QVM with QPU
qpu = QVMConnection()

# noise acorn; qpu = QVMConnection()


#qpu = QPUConnection(acorn)

qubits = [8,13]
gate = SWAP 
gate_str = 'SWAP'
numberSamples = 500
numberSamplesQVM = 1000



def compile_INIT_gate(prog):
     compiler = CompilerConnection(acorn)
     compiledProg = compiler.compile(prog)
     qpuProg = Program()
     qpuProg.inst(compiledProg)

     return qpuProg



def process_tomography(Program, numberSamples, qubits):
    process_tomography_qpu, _, _ = do_process_tomography(
        Program, numberSamples, qpu, qubits)
    process_tomography_qvm, _, _ = do_process_tomography(
        Program, numberSamplesQVM, qvm, qubits)

    print('The process matrix:\n', process_tomography_qpu.to_chi())
    with open('processmatrix_qpu_' + gate_str + '_' + str(qubits[0]) + '_' + str(numberSamples) + '.txt', 'w') as text_file:
        print("QPU Estimated process matrix: {}".format(process_tomography_qpu.to_chi()), file=text_file)

    process_fidelity = process_tomography_qpu.avg_gate_fidelity(
        process_tomography_qvm.r_est)
    print('The estimate process fidelity is:', process_fidelity)

    qpu_plot = process_tomography_qpu.plot()
    qpu_plot.text(0.4, .95, r'$F_{{\rm avg}}={:1.1f}\%$'.format(process_fidelity * 100), size=25)

    plt.savefig('process_tomography_qpu_' + gate_str + '_' + str(qubits[0]) + '_' + str(numberSamples) + '.png')
    process_tomography_qvm.plot()
    plt.savefig('process_tomography_qvm_' + gate_str + '_' + str(qubits[0]) + '_' + str(numberSamplesQVM) + '.png')

def qvm_chi_matrix(Program, numberSamples, qubits):
    process_tomography_qvm, _, _ = do_process_tomography(
        Program, numberSamplesQVM, qvm, qubits)

    print('The process matrix:\n', process_tomography_qvm.to_chi())
    with open('processmatrix_qvm_' + gate_str + '_' + str(qubits[0]) + '_' + str(numberSamples) + '.txt', 'w') as text_file:
        print("QVM Estimated process matrix: {}".format(process_tomography_qvm.to_chi()), file=text_file)




prog = Program()
prog.inst(gate(qubits[0],qubits[1]))
prog = compile_INIT_gate(prog)
#process_tomography(prog, numberSamples, qubits)
qvm_chi_matrix(prog, numberSamples, qubits)

