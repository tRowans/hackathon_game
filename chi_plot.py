import numpy as np
import matplotlib.pyplot as plt

def extract_matrix(path):
    with open(path) as f:
        line = f.readline() #skip header
        line = f.readline()
        line = f.readline()
        chi = []
        current_row = []
        count = 0
        while line:
            try:
                if line[2] == " ":
                    line = line[3:-1]
                else:
                    line = line[2:-1]
                current_row += line.split()
                if current_row[-1][-1] == "]":
                    if current_row[-1][-2] == "]":
                        current_row[-1] = current_row[-1][:-1]
                    current_row[-1] = current_row[-1][:-1]
                    for i in range(len(current_row)):
                        current_row[i] = complex(current_row[i])
                    chi.append(current_row)
                    current_row = []
                line = f.readline()
                count += 1
            except:
                print(path)
                print(count)
    return np.array(chi)

#qvm = abs(extract_matrix("processmatrix_qvm_H_8_2000.txt"))
qpu = abs(extract_matrix("processmatrix_qpu_CNOT_8_13_500.txt"))
#plt.imshow(qvm,cmap='Greys')
plt.imshow(qpu,cmap='Greys')
cbar = plt.colorbar()
cbar.set_label('Difference in Absolute Matrix Elements',rotation=270,labelpad=15)
plt.tick_params(
    axis = 'both',
    which = 'both',
    bottom = False,
    top = False,
    labelbottom = False,
    right = False,
    left = False,
    labelleft = False
    )
plt.show()
