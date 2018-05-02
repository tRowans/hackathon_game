from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection
import numpy
import random
from scipy.stats import chisquare 
from random import shuffle

def gen_layer(gate_shop, qubits):
    layer = []
    cash = len(qubits)
    sites = qubits.copy()
    while cash > 0:
        pick = random.choice(list(gate_shop.keys()))
        if gate_shop[pick] <= cash:
            layer.append(pick)
            cash -= gate_shop[pick]
    for i in range(len(layer)):
        gate_sites = random.sample(sites, gate_shop[layer[i]])
        sites = [x for x in sites if x not in gate_sites]
        layer[i] = layer[i](*gate_sites)
    return layer

def gen_circuit(qubits, depth):
    gate_shop = {I:1, X:1, Z:1, H:1, CNOT:2} #Gates are keys, costs are values
    circuit = []
    for i in range(depth):
        circuit.append(gen_layer(gate_shop,qubits))
    return circuit

def genQUIL(layers,qubits): #takes a list of gates in format [[H(1),I(2)],[H(2),I(1)],[CNOT(1,2),Y(3)]] converts to QUIL

    program = Program()

    for layer in layers:
       program.inst(layer)
    
    for i in qubits:
        program.measure(i,i)

    return program

def string_checker(string,measurement):
    for i in range(len(string)):
        if int(string[i]) != measurement[i]:
            return 0
    return 1

def get_dist(program,qubits):
    bits = [x for x in range(len(qubits))]
    strs = [bin(x)[2:].zfill(len(qubits)) for x in range(2**len(qubits))]
    probs = []
    qvm = QVMConnection()
    out = qvm.run(program, bits, trials=10000)
    for i in strs:
        matches = [x for x in out if string_checker(i,x)]
        probs.append(len(matches)/len(out))
        print("String {} occurs with probability {}".format(i,probs[-1]))
    return probs

def Compare_stats(dist_user,dist_ref): #function takes user and reference distributions in format [0.8,0.4,0.7] and compares them.
    for i in range(len(dist_user)):
        comp = abs(dist_user[i]-dist_ref[i])
        if comp > 0.01:
            return 0
    return 1
