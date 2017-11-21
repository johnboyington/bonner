'''
Compares the 8in data in DECKER's paper with that found using my own calculations.
'''

import numpy as np
import matplotlib.pyplot as plt

decker_data = np.loadtxt('decker_data.txt')
my_data = np.loadtxt('all_response_data.txt')

#pull the energy groups from my data
erg_groups = my_data[0:26,1]

#normalize my data using the coefficient from decker for 8" spheres
norm = [1.400E-04, 1.774E-02, 3.990E-02, 1.109E-01, 2.838E-01, 4.435E-01, 6.386E-01]
spheres = [[ 0,      'k', 'Bare LiI(Eu) Detector', 's'],
           [ 2,      'r',           ' 2in Sphere', 'o'],
           [ 3,      'b',           ' 3in Sphere', '^'],
           [ 5,      'm',           ' 5in Sphere', 'v'],
           [ 8,      'g',           ' 8in Sphere', 'D'],
           [10,   'navy',           '10in Sphere', '<'],
           [12, 'purple',           '12in Sphere', '>'],]



###############################################################################
#                        PLOTTING BOYINGTON RESPONSES
###############################################################################
#open figure and set parameters
plt.figure(0)
plt.xscale('log')
plt.yscale('log')
plt.xlim(1.0E-8, 26)
plt.ylim(1.0E-5, 0.25)
plt.title('Boyington Bonner Sphere Response Functions')
plt.xlabel('Energy (MeV)')
plt.ylabel('Response (cm$^{2}$)')

#plot my data
for sphere in range(7):
    L = sphere * 26
    R = (sphere + 1) * 26
    data = my_data[L:R]
    data[:,2] *= norm[sphere]
    plt.plot(erg_groups, data[:,2], color=spheres[sphere][1], label=spheres[sphere][2], marker=spheres[sphere][3], fillstyle=u'none')
    plt.errorbar(erg_groups, data[:,2], data[:,2] * data[:,3], color=spheres[sphere][1], linestyle="None")


plt.legend()
plt.savefig('boyington_response_functions.png', dpi=200)
plt.close()


###############################################################################
#                        PLOTTING DECKER RESPONSES
###############################################################################
#open figure and set parameters
plt.figure(1)
plt.xscale('log')
plt.yscale('log')
plt.xlim(1.0E-8, 26)
plt.ylim(1.0E-5, 0.25)
plt.title('Decker Bonner Sphere Response Functions')
plt.xlabel('Energy (MeV)')
plt.ylabel('Response (cm$^{2}$)')

s = ''
#plot decker data
for sphere in range(7):
    L = sphere * 26
    R = (sphere + 1) * 26
    data = decker_data[L:R]
    plt.plot(erg_groups, data[:,0], color=spheres[sphere][1], label=spheres[sphere][2], marker=spheres[sphere][3], fillstyle=u'none')
    plt.errorbar(erg_groups, data[:,0], data[:,0] * data[:,1], color=spheres[sphere][1], linestyle="None")
    for i, g in enumerate(erg_groups):
        s += '{:2d}   {:14.8e}   {:14.8e}   {:14.8e} \n'.format(spheres[sphere][0], g, data[i][0], data[i][1])
with open('decker_data_new.txt', 'w+') as f:
    f.write(s)


plt.legend()
plt.savefig('decker_response_functions.png', dpi=200)
plt.close()

###############################################################################
#                      COMPARING INDIVIDUAL RESPONSES
###############################################################################


for i, sphere in enumerate(spheres):
    L = i * 26
    R = (i + 1) * 26
    b_data =  my_data[L:R, 2:4]
    d_data = decker_data[L:R]
    
    plt.figure(i + 10)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1.0E-8, 26)
    plt.ylim(1.0E-5, 0.25)
    plt.title('{} in Sphere Comparison'.format(sphere[0]))
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Response (cm$^{2}$)')

    plt.plot(erg_groups, b_data[:,0], color='r', label='Boyington')
    plt.errorbar(erg_groups, b_data[:,0], b_data[:,0] * b_data[:,1], color='r', linestyle="None")
    plt.plot(erg_groups, d_data[:,0], color='k', label='Decker')
    plt.errorbar(erg_groups, d_data[:,0], d_data[:,0] * d_data[:,1], color='k', linestyle="None")
    
    plt.legend()
    plt.savefig('{}_in_sphere_comparison.png'.format(sphere[0]), dpi=200)
















