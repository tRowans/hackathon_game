from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
import random
from scipy.stats import chisquare 
from random import shuffle

def gen_layer(gate_shop, qubits):
    layer = []
    cash = qubits
    sites = list(numpy.arange(0,qubits,1))
    while cash > 0:
        pick = random.choice(list(gate_shop.keys()))
        if gate_shop[pick] <= cash:
            layer.append(pick)
            cash -= gate_shop[pick]
    for i in range(len(layer)):
        gate_sites = random.sample(sites, gate_shop[layer[i]])
        sites = [x for x in sites if x not in gate_sites]
        layer[i] = layer[i](eval(str(gate_sites)[1:-1]))
    return layer

def gen_circuit(qubits, depth):
    gate_shop = {I:1, X:1, Y:1, Z:1, H:1} #Gates are keys, costs are values
    circuit = []
    for i in range(depth):
        circuit.append(gen_layer(gate_shop,qubits))
    return circuit

def genQUIL(layers): #takes a list of gates in format [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]] converts to QUIL

    program = Program()

    for layer in layers:

       program.inst(layer)

    return program

def string_checker(string,measurement):
    for i in range(len(string)):
        if int(string[i]) != measurement[i]:
            return 0
    return 1

def get_dist(program,qubits):
    bits = [x for x in range(qubits)]
    strs = [bin(x)[2:].zfill(qubits) for x in range(2**qubits)]
    probs = []
    qvm = QVMConnection()
    out = qvm.run(program, bits, trials=100)
    for i in strs:
        matches = [x for x in out if string_checker(i,x)]
        probs.append(len(matches)/len(out))
        print("String {} occurs with probability {}".format(i,probs[-1]))
    return probs


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

def User_circuit(problem,depth):#function presents user with available gates and makes them create their circuit layer by layer.

    available_gates=[]
    for gate in problem.instructions:
        available_gates.append(gate.name)
    
    shuffle(available_gates)

    solution=Program()

    for layer in range(depth):
        print ('layer',layer)
        print ('Available gates:')
        print(available_gates)
        gates = input("Please enter gates in layer" + str(layer) + "in format[GATE qubit,GATE qubit]:")
        print()

        gates.split(' ', 1)
        layer = gates.split(",")

        for gate in layer:
            if gate.split(' ', 1)[0] in available_gates: 
                available_gates.remove(gate.split(' ', 1)[0])  
                solution.inst(gate)  
            else:
                print("Gate choice," +  gate + "not available")
        
    return solution


def menu():
    print("--------MENU--------")
    print("Play tutorial (1)")
    print("Play random (2)")
    print("Exit (3)")
    print("--------------------")
    selection = int(input("Please choose: "))

    if selection == 1:
       #run the tutorial
      print("not available yet")
    if selection == 2:
      random_circuit()
    if selection == 3:
      exit()

def user_attempt(problem,problem_stats,depth,qubits):
    solution = User_circuit(problem,depth)
    solution_stats = get_dist(solution,qubits)
    result = Compare_stats(solution_stats,problem_stats)
    success = Test_for_victory(result,0.95)

    return success

def random_circuit():
    qubits = int(input("Number of qubits:"))
    depth = int(input("Circuit depth:"))

    circa = gen_circuit(qubits,depth)
    problem = genQUIL(circa)
    print (problem)
    problem_stats = get_dist(problem,qubits)     #THESE WILL BE REPLACED BY FUNCTIONS WHICH TAKE SOLUTION AND PROBLEM AS INPUTS
    print(problem_stats)

    res = user_attempt(problem,problem_stats,depth,qubits)
    
    print (res)

menu()


