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
       #run the tutorial
      print("not available yet")
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

menu()
