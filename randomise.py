from pyquil.quil import *
from pyquil.gates import *
from pyquil.api import QVMConnection,CompilerConnection
import numpy
import random
import math as m
from scipy.stats import chisquare 
from pyquil.device import ISA

def gen_H(qubit_list):
    choice_list = qubit_list
    target = random.choice(choice_list)
    prog_H = Program()
    prog_H.inst(RZ(m.pi/2.0,target)).inst(RX(m.pi/2.0,target)).inst(RZ(m.pi/2.0,target))

    return prog_H

def gen_X(qubit_list):

    prog_X = Program()
    prog_X.inst(RX(-m.pi,qu))

    return prog_X


def gen_Z(qubit_list):
    choice_list = qubit_list
    target = random.choice(choice_list)
    prog_Z = Program()
    prog_Z.inst(RZ(m.pi,target))


    return prog_Z

def gen_CZ(qubit_list):
    choice_list = qubit_list
    target = random.choice(choice_list)
    choice_list.remove(target)
    control = random.choice(choice_list)

    prog_Z = Program()
    prog_Z.inst(CZ(target,control))


    return prog_Z

gate_list = [gen_H,gen_X,gen_Z]
qubit_list = [8]
seq_length = 10
seq_attempts =10
seq_trials = 10

sequence = Program()
for j in range (0,seq_attempts):
    clear_prog = Program()
    sequence = clear_prog
    for i in range (0,seq_length):
         foo_prog = random.choice(gate_list)(qubit_list)
         sequence.inst(foo_prog)

    sequence_inverse = sequence.dagger()

    sequence.inst(sequence_inverse)
    sequence.inst(MEASURE(8,0))

    qvm = QVMConnection()
    out = qvm.run(sequence, [0], seq_trials)
    sum=0
    for x in out:
        if (x[0] == 0):
              sum = sum +1

    print(float(sum)/float(seq_trials))
    print(sequence)