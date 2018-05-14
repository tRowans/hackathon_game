from pyquil.quil import *
from pyquil.gates import *
from pyquil.api import QVMConnection,QPUConnection, get_devices
import numpy
import random
import math as m
from scipy.stats import chisquare 
from pyquil.device import ISA
import pickle


def gen_H(qubit_list):
    choice_list = list(qubit_list)
    target = random.choice(choice_list)
    prog_H = Program()
    prog_H.inst(RZ(m.pi/2.0,target)).inst(RX(m.pi/2.0,target)).inst(RZ(m.pi/2.0,target))

    return prog_H

def gen_X(qubit_list):
    choice_list = list(qubit_list)
    target = random.choice(choice_list)
    prog_X = Program()
    prog_X.inst(RX(-m.pi, target))

    return prog_X


def gen_Z(qubit_list):
    choice_list = list(qubit_list)
    target = random.choice(choice_list)
    prog_Z = Program()
    prog_Z.inst(RZ(m.pi,target))


    return prog_Z

def gen_CZ(qubit_list):

    choice_list = list(qubit_list)
    target = random.choice(choice_list)
    choice_list.remove(target)
    control = random.choice(choice_list)

    prog_Z = Program()
    prog_Z.inst(CZ(target,control))

    return prog_Z

def Fidelity(seq_length,seq_trials, gate_list, qubit_list,qpu):

    sequence = Program()
 
    for i in range (0,seq_length):
         foo_prog = random.choice(gate_list)(qubit_list)
         sequence.inst(foo_prog)
    
    prog = Program()
    prog.inst(("PRAGMA PRESERVE_BLOCK"))
    prog.inst(sequence)
    prog.inst(sequence.dagger())
    prog.inst(MEASURE(8,0))
    prog.inst(MEASURE(13,1))
    prog.inst(("PRAGMA END_PRESERVE_BLOCK"))

    out = qpu.run(prog, [0,1], seq_trials)
    sum=0
    for x in out:
        if (x[0] == 0 and x[1]==0):
              sum = sum +1
    return(float(sum)/float(seq_trials))
    print(sum)

gate_list = [gen_X,gen_Z]
qubit_list = [13]

seq_trials = 500   #how many times to test each sequence
num_of_seqs  = 20 #number of sequences of a given length to try

range_of_seqs = range(0,200)  #every 10 up to 200
interval = 5


acorn = get_devices(as_dict=True)['19Q-Acorn']

qvm = QVMConnection(acorn)


data=[]
len_list=[]
ave_fid=[]

for length in range_of_seqs[::interval]:
    print (length)
    data=[]
    for j in range (0,num_of_seqs):
        data.append(Fidelity(length, seq_trials, gate_list, qubit_list,qvm))
    len_list.append(length)
    print(sum(data) / float(len(data)))
    ave_fid.append(sum(data) / float(len(data)))


with open("len_list_single13.txt", "wb") as fp:   #Pickling
      pickle.dump(len_list, fp)

with open("ave_fid_single13.txt", "wb") as fp:   #Pickling
      pickle.dump(ave_fid, fp)


