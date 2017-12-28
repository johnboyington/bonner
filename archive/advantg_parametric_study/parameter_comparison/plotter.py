'''
This code will take data from the bonner sphere parametric study and plot it.
Initialized: 7/10/17 by John Boyington

Inputs:
    - data.txt which contains info on advantg voxel sizes, mcnp FOMs, and runTimes
    
Outputs:
    - plots comparing FOM and corrected FOMs for each voxel size
'''

import numpy as np
import matplotlib.pyplot as plt


# [filename, sphere size, incident energy, collapse factor]

filelist = [['5in_6e-8mev_data.txt', 5, 6E-8, 1], 
            ['5in_6e-8mev_data.txt', 5, 6E-8, 1]]

for files in filelist:
    data = np.loadtxt(files[0])
    print data
    plt.figure(0)
    plt.title('Comparison of mcnp FOMs')
    plt.xlabel('Voxel size (cm$^3$)')
    plt.ylabel('FOM')
    plt.plot(data[:,0], data[:,1], label='{:2d} inch {:4.3e} MeV'.format(files[1], files[2]), color='seagreen')
    plt.legend()
    plt.savefig('advantg_parametric_study.png')
    plt.close()
