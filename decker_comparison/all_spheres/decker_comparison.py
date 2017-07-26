'''
Compares the 8in data in DECKER's paper with that found using my own calculations.
'''

import numpy as np
import matplotlib.pyplot as plt

decker_data = np.loadtxt('decker_data_8in.txt')
my_data = np.loadtxt('response_data_8in.txt')

#pull the energy groups from my data
erg_groups = my_data[:,1]

#normalize my data using the coefficient from decker for 8" spheres
norm = 2.838E-01
my_data[:,2] *= norm

#open figure and set parameters
plt.figure(0)
plt.xscale('log')
plt.title('Comparison of 8" Bonner Sphere Response Functions')
plt.xlabel('Energy MeV')
plt.ylabel('Response cm$^{2}$')


#plot my data
plt.plot(erg_groups, my_data[:,2], color='mediumblue', label='Boyington')
plt.errorbar(erg_groups, my_data[:,2], my_data[:,2] * my_data[:,3], color='mediumblue', linestyle="None")

#plot decker's data
plt.plot(erg_groups, decker_data[:,0], color='mediumseagreen', label='Decker')
plt.errorbar(erg_groups, decker_data[:,0], decker_data[:,0] * decker_data[:,1], color='mediumseagreen', linestyle="None")

plt.legend()
plt.savefig('8in_comparison.png', dpi=200)