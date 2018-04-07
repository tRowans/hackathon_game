from pyquil.quil import Program
from pyquil.gates import H, CNOT,...
from pyquil.api import QVMConnection
import numpy

def genQUIL(layers):

    program = Program()

    for layer in layers:

       program.inst(layer)

    return program