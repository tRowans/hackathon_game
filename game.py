from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy

def genQUIL(layers):

    program = Program()

    for layer in layers:

       program.inst(layer)

    return program


test_circuit = [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]]

prog = genQUIL(test_circuit)

print (prog)