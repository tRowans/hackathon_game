from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
from scipy.stats import chisquare 
from random import shuffle

def genQUIL(layers): #takes a list of gates in format [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]] converts to QUIL

    program = Program()

    for layer in layers:

       program.inst(layer)

    return program

def Compare_stats(dist_user,dist_ref): #function takes user and reference distributions in format [0.8,0.4,0.7] and compares them.

    result = chisquare(dist_user,dist_ref)
    
    return result

def Test_for_victory(result,tolerance):  #takes the results of stats test and the required tolerance of success 
    success = False

    if (result[1] > tolerance):
        success = True
    else:
        success = False 

    return success

def jake_test():  #probably bad practise to put my test here but oh well.


    test_user = [0.8,0.4,0.7]
    test_ref = [0.6,0.3,0.2]
    test_circuit = [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]]

    prog = genQUIL(test_circuit)
    res = Compare_stats(test_user,test_ref)
    suc = Test_for_victory(res,0.95)
    print (prog,res[1],suc)

def User_circuit(gates,depth,program):#function presents user with available gates and makes them create their circuit layer by layer.

    available_gates=[]
    available_qubits= range(0,depth)
    for gate in program.instructions:
        available_gates.append(gate.name)
    

    shuffle(available_gates)

    for layer in range(depth):
        print ('layer',layer)
        print ('Available gates:')
        print(available_gates)
        print ('Available quits:')
        print(available_qubits)



test_circuit = [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]]
trial_gates = [H(1),CNOT(1,2),Y(3)]
test_user = [0.8,0.4,0.7]
test_ref = [0.6,0.3,0.2]
prog = genQUIL(test_circuit)
res = Compare_stats(test_user,test_ref)
suc = Test_for_victory(res,0.95)
User_circuit(trial_gates,3,prog)