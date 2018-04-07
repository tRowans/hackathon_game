from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
from scipy.stats import chisquare 

def genQUIL(layers):

    program = Program()

    for layer in layers:

       program.inst(layer)

    return program


def compare_stats(dist_user,dist_ref): #function takes user and reference distributions and compares them.

    result = chisquare(dist_user,dist_ref)
    

    return result




test_user = [0.8,0.4,0.7]
test_ref = [0.78,0.39,0.71]

test_circuit = [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]]

prog = genQUIL(test_circuit)
res = compare_stats(test_user,test_ref)
print (prog)
print(res)