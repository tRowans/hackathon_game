from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
import random
from scipy.stats import chisquare 
from random import shuffle
from gen_levels import *

def layer_input(layer,available_gates,solution):
    print()
    print ('layer',layer)
    print ('Available gates:')
    print(available_gates)
    gates = input("Please enter gates in layer " + str(layer) + " in format GATE qubit,GATE qubit,...:")
    print()

    gatelist = gates.split(",")
    used_qubits = []

    for gate in gatelist:
        if gate.split(' ')[0] not in available_gates:
            print("Gate choice " + gate + " not available")
            layer_input(layer,available_gates,solution)
        if len(gate.split(' ')) == 1:
            print("All gates must take at least one qubit as an argument")
            layer_input(layer,available_gates,solution)
        for i in gate.split(' ')[1:]:
            try:
                inti = int(i)
            except ValueError:
                print("Please enter a valid qubit index")
                layer_input(layer,available_gates,solution)
            if i in used_qubits:
                print("Qubits may only be used once per layer")
                layer_input(layer,available_gates,solution)
            else:
                used_qubits.append(i)

    for gate in gatelist: 
        if gate.split(' ')[0] in available_gates: 
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

def select():
    try:
        selection = int(input("Please choose: "))
    except ValueError:
        print("Invalid input")
        select()
        
    if selection == 1:
        print("not available yet")
        select()
    elif selection == 2:
        random_circuit()
    elif selection == 3:
        exit()
    else:
        print("Invalid input")
        select()

def menu():
    print("\n\n")
    print("--------MENU--------")
    print("Play tutorial (1)")
    print("Play random (2)")
    print("Exit (3)")
    print("--------------------")
    select()

def retry(problem,problem_stats,depth,qubits):
    again = input("Try again (1) or see solution (2):")
    try:
        again = int(again)
    except ValueError:
        print("Invalid input")
        retry(problem,problem_stats,depth,qubits)
    if again == 1:
        user_attempt(problem,problem_stats,depth,qubits)
    elif again == 2:
        print("Solution is:")
        for i in range(qubits):
            problem.pop()
        print(problem)
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

def input_qubits():
    try:
        in_q = int(input("Number of qubits:"))
    except ValueError:
        print("Invalid input")
        input_qubits()
    return in_q

def input_depth():
    try:
        in_d = int(input("Circuit depth:"))
    except ValueError:
        print("Invalid input")
        input_depth()
    return in_d

def random_circuit():
    print()
    qubits = input_qubits()
    depth = input_depth()
    print()

    circa = gen_circuit(qubits,depth)
    problem = genQUIL(circa,qubits)
    problem_stats = get_dist(problem,qubits)     
    user_attempt(problem,problem_stats,depth,qubits)

menu()
