from pyquil.quil import Program
from pyquil.gates import H
from pyquil.api import QVMConnection
import numpy
import random

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
        layer[i] = layer[i]+"("+str(gate_sites)[1:-1]+")"
    return layer

def gen_circuit(qubits, depth):
    gate_shop = {"I":1, "X":1, "Y":1, "Z":1, "H":1} #Gates are keys, costs are values
    circuit = []
    for i in range(depth):
        circuit.append(gen_layer(gate_shop,qubits))
    return circuit
