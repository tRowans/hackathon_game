from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
import random
from scipy.stats import chisquare 
from random import shuffle
from gen_levels import *

def layer_input(layer,available_gates,solution):
    print ('layer',layer)
    print ('Available gates:')
    print(available_gates)
    gates = input("Please enter gates in layer " + str(layer) + " in format GATE qubit,GATE qubit:")
    print()

    gatelist = gates.split(",")
    print(gatelist)

    for gate in gatelist:
        if gate.split(' ', 1)[0] not in available_gates:
            print("Gate choice " + gate + " not available")
            layer_input(layer,available_gates)
        

    for gate in gatelist: 
        if gate.split(' ', 1)[0] in available_gates: 
            available_gates.remove(gate.split(' ', 1)[0])  
            solution.inst(gate)  
    return solution

def User_circuit(problem,depth,qubits):#function presents user with available gates and makes them create their circuit layer by layer.

    available_gates=[]
    for gate in problem.instructions[:-qubits]:
        available_gates.append(gate.name)
    
    shuffle(available_gates)

    solution=Program()

    for layer in range(depth):
        solution = layer_input(layer,available_gates,solution)

    for i in range(qubits):
        solution.measure(i,i)
        
    return solution


def menu():
    print("\n\n\n\n\n")
    print("--------MENU--------")
    print("Play tutorial (1)")
    print("Play random (2)")
    print("Exit (3)")
    print("--------------------")
    selection = int(input("Please choose: "))

    if selection == 1:
       tutorial()
    if selection == 2:
      random_circuit()
    if selection == 3:
      exit()

def retry(problem,problem_stats,depth,qubits):
    again = input("Try again (y/n)?")
    if again == 'y' or 'Y':
        user_attempt(problem,problem_stats,depth,qubits)
    elif again == 'n' or 'N':
        menu()
    else:
        print("Invalid input")
        retry()

def user_attempt(problem,problem_stats,depth,qubits):
    solution = User_circuit(problem,depth,qubits)
    solution_stats = get_dist(solution,qubits)
    success = Compare_stats(solution_stats,problem_stats)
    if success:
        print("Congratulations, you are correct!")
        menu()
    else:
        print("Incorrect")
        retry(problem,problem_stats,depth,qubits)

def random_circuit():
    qubits = int(input("Number of qubits:"))
    depth = int(input("Circuit depth:"))

    circa = gen_circuit(qubits,depth)
    problem = genQUIL(circa,qubits)
    problem_stats = get_dist(problem,qubits)     
    res = user_attempt(problem,problem_stats,depth,qubits)
    if res:
        print("Congratulations, you are correct!")
        menu()
    else:
        retry = input("Incorrect. Try again? (y/n)")
        if retry == 'y' or 'Y':
            function
        elif retry == 'n' or 'N':
            menu()
        else:
            print("That is not a valid response")

def tutorial():

 

    level1()
    level2()
    level3()
    level4()



def level1():
    circuit = Program()
    initz = Program()

    circuit.inst(H(0))
    circuit.inst(Z(0))
    circuit.inst(H(0))
    circuit.inst(MEASURE(0,0))

    initz.inst()

    qubits = 1
    depth = 3

    introduction = "The state is initialised as |0>.Bit flips are most efficiently implemented using Pauli X gates. Construct an equivalent circuit using the following three gates: Z,H,H"
    conclusion = "A Z gate sandwiched between two H gates is an equivalent circuit"
    hint = "I like sandwiches"
    level1 = level(1,3,circuit,initz,introduction,conclusion,hint)

def level2():
    circuit = Program()
    initz = Program()

    circuit.inst(H(1))
    circuit.inst(CZ(0,1))
    circuit.inst(H(1))
    circuit.inst(MEASURE(0,0))
    circuit.inst(MEASURE(1,1))

    initz.inst(X(0))


    qubits = 2
    depth = 3

    introduction = "The state is initialised as |1,0>. Apply the following gates to construct a CNOT gate:"
    conclusion = "Applying two H gates on the target qubit, which are sandwiching the CZ gate, results in cancelling of the H gates when the control is zero and a NOT gate when the control is 1."
    hint = "I like sandwiches"
    level2 = level(qubits,depth,circuit,initz,introduction,conclusion,hint)


def level3():
    circuit = Program()
    initz = Program()

    circuit.inst(H(1))
    circuit.inst(H(0))

    circuit.inst(CNOT(0,1))
    circuit.inst(H(1))
    circuit.inst(H(0))
    circuit.inst(MEASURE(0,0))
    circuit.inst(MEASURE(1,1))

    initz.inst(X(1))


    qubits = 2
    depth = 3

    introduction = "The state is initialised as |0,1>. Reverse the control and target qubit of the CNOT gate using the following gates:"
    conclusion = "A CNOT gate with four H gates, one before and one after the control and one before and one after the target, is equivalent to a CNOT operation where control and target are exchanged"
    hint = "I like sandwiches"
    level3 = level(qubits,depth,circuit,initz,introduction,conclusion,hint)


def level4():
    circuit = Program()
    initz = Program()

    circuit.inst(CNOT(0,1))
    circuit.inst(H(1))
    circuit.inst(H(0))

    circuit.inst(CNOT(0,1))
    circuit.inst(H(1))
    circuit.inst(H(0))

    circuit.inst(CNOT(0,1))

    circuit.inst(MEASURE(0,0))
    circuit.inst(MEASURE(1,1))

    initz.inst(X(0))


    qubits = 2
    depth = 5

    introduction = "The state is initialised as |1,0>. Create a SWAP gate using the following gates:"
    conclusion = "Applying the reversed CNOT circuit between two CNOT gates creates the SWAP operation where the final state is: |0,1>. Alternatively a CNOT between two reversed CNOT gates creates a SWAP gate."
    hint = "I like sandwiches"
    level3 = level(qubits,depth,circuit,initz,introduction,conclusion,hint)


class level:
    def __init__(self,qubits,depth,circuit,initial,introduction,conclusion,hint):
        self.qubits = qubits
        self.depth = depth
        self.circuit = circuit 
        self.initial = initial 
        self.hint = hint
        self.introduction = introduction
        self.conclusion = conclusion
        self.stats = get_dist((self.initial + self.circuit),self.qubits)
 
        print(self.introduction)
        print("Problem has depth " + str(self.depth) + " and number of qubits" + str(self.qubits))
        self.attempt() 
  
    def attempt(self):
        solution = self.initial + User_circuit(self.circuit,self.depth,self.qubits)
        solution_stats = get_dist(solution,self.qubits)
        success = Compare_stats(solution_stats,self.stats)

        if success:
            print("Congratulations, you are correct!")
            print(self.conclusion)

            retry = input("Next Level? (y/n)")
            if retry == 'y' or retry == 'Y':
                    pass
            else:
                    menu()
        else:
            print("Incorrect")
            retry = input("Incorrect, would you like to try again? (y/n)")
            if retry == 'y' or retry == 'Y':
                    self.attempt()
            else:
                    menu()



menu()
