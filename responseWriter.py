#this code will write the mcnp6 input files used to find the Bonner Sphere response
#functions

import numpy as np
import matplotlib.pyplot as plt
import os

#create a directory to put mcnp input files into
try:
    os.mkdir('output')
except OSError,e:
    print e

#this array contains the bonner sphere diameters in inches
sizeinch = np.array([0, 2, 3, 5, 8, 10, 12])

#convert the bonner sphere diameters into radii in cm
size = (sizeinch * 2.54) / 2.

#this is the energy bins used in the source term
eq = np.array([1.00000000e+07,   3.67900000e+06,   1.35300000e+06,
               5.00000000e+05,   4.08500000e+04,   9.11800000e+03,
               1.48729000e+02,   4.80520000e+01,   1.59680000e+01,
               9.87700000e+00,   4.00000000e+00,   3.30000000e+00,
               2.60000000e+00,   2.10000000e+00,   1.30000000e+00,
               1.15000000e+00,   1.09700000e+00,   1.02000000e+00,
               9.72000000e-01,   9.50000000e-01,   8.50000000e-01,
               6.25000000e-01,   4.00000000e-01,   3.20000000e-01,
               2.50000000e-01,   1.80000000e-01,   1.40000000e-01,
               1.00000000e-01,   8.00000000e-02,   5.00000000e-02,
               3.00000000e-02,   1.50000000e-02,   1.00000000e-05, 0])

#this reverses the erg bins becuase I copied them backwards
eb = eq[::-1]

#these are the cosine bins used by the source terms
cb = np.array([180, 90, 80, 70, 60, 50, 40, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

#calculate the width of each cosine bin
cbw = cb[:-1] - cb[1:]

#reversing the cosine bins
cbr = cb[::-1]

#the factor to convert deg to rad
f = np.pi / 180.

#calculates the cosine value of each bin
ab = np.cos(cb * f)

#reads in the neutron source flux data from the mcnp output file
ndata = np.loadtxt('ndata.txt')[:,1:].T

#reshapes the neutron data into an array
nfl = ndata[0].reshape(len(cbw),-1).T

#calculates the total neutron flux for each energy bin
netot = np.sum(nfl, axis=1)


'''
This function creates the source term for the bonner sphere mcnp input file

It uses the cosine bin data from the given energy group to write the source distribution

Inputs:
    numb - the energy group number
    ee - the energy group's lower bound (MeV)
    eee - the energy group's upper bound (MeV)
'''
def Source(numb, ee, eee):
    #first value in SP card must be zero, so add a zero to the cosine data
    d = np.concatenate((np.array([0]), nfl[numb]), axis=0)
    H = ''
    H += 'c  ---------------------------------------------------------\n'
    H += 'c                    SOURCE SPECIFICATIONS\n'
    H += 'c  ---------------------------------------------------------\n'
    H += 'SDEF   POS=-15.24 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG=D1\n'
    H += '       DIR=D5 RAD=D6 PAR=1\n'
    H += 'SI1   {} {}\n'.format(ee, eee)
    H += 'SP1   0  1\n'
    H += 'SI6   0  1.27\n'
    H += 'SP6 -21  1\n'
    for ii in range(len(ab) / 4):    
        if ii == 0 : card = 'SI5 H  '
        else: card = '        '         
        H += '{}  {:10.5e} {:10.5e} {:10.5e} {:10.5e}\n'.format(card, ab[ii * 4], ab[ii * 4 + 1], ab[ii * 4 + 2], ab[ii * 4 + 3])
    for ii in range(len(ab) / 4):    
        if ii == 0 : card = 'SP5 D   '
        else: card = '        '         
        H += '{}  {:10.5e} {:10.5e} {:10.5e} {:10.5e}\n'.format(card, d[ii * 4], d[ii * 4 + 1], d[ii * 4 + 2], d[ii * 4 + 3])
    return H

#writes the sphere card for the mcnp input
def Sphere(big):
    H = ''
    H = '01  S   0 0 -0.9  {}    $Bonner Sphere\n'.format(big)
    return H

'''
The next 3 functions just read in the mcnp input file data for different cards
that exist in text files in this directory. They are constant for each problem.
'''
def Card0():
    H = ''
    H = open('card0.txt', 'r').read()
    return H
def Card1():
    H = ''
    H = open('card1.txt', 'r').read()
    return H
def Card2():
    H = ''
    H = open('card2.txt', 'r').read()
    return H

#this function names the mcnp input file
def Name(big, erg):
    N = 's{}e{}'.format(big, erg)
    return N


#this creates a qsub file for each input file for submission to eigendoit
def subFile(name):
    H = '#!/bin/sh\n'
    H += '#PBS -l nodes=1:ppn=32\n'
    H += 'cd $PBS_O_WORKDIR\n'
    H += 'cat $PBS_NODEFILE > nodes\n'
    H += "NO_OF_CORES=`cat $PBS_NODEFILE | egrep -v '^#'\|'^$' | wc -l | awk '{print $1}'`\n"
    H += 'echo $NO_OF_CORES\n'
    H += 'NODE_LIST=`cat $PBS_NODEFILE`\n'
    H += 'echo $NODE_LIST\n'
    H += 'mpirun -np $NO_OF_CORES -machinefile nodes mcnp6.mpi i={}.i run={}.ru o={}.o\n'.format(name, name, name)
    return H

#this function creates a bash file to submit all of the qsub files for each mcnp input
def bashFile(diameter, energy):
    H = '#!/bin/bash\n'
    H += 'declare -a siz=('
    for ii in diameter:
        H += '{} '.format(ii)
    H += ')\n'
    H += 'declare -a erg=('
    for jj in energy:
        H += '{} '.format(jj)
    H += ')\n'
    H += 'for G in "${siz[@]}"\n'
    H += 'do\n'
    H += '        for H in "${erg[@]}"\n'
    H += '        do\n'
    H += "                echo 'Submitting' 's'$G'e'$H\n"
    H += "                qsub 's'$G'e'$H.qsub\n"
    H += '        done\n'
    H += 'done\n'
    return H
    
#set parameters
erg = range(len(eb) - 1)
dia = range(len(size))

#loop through each energy group and sphere size
for ii in dia:
    for jj in erg:
        s = ''
        s += Card0()
        s += Sphere(size[ii])
        s += Card1()
        s += Source(jj, eb[jj], eb[jj + 1])
        s += Card2()
        t = ''
        t += subFile(Name(ii, jj))
        with open('output/{}.i'.format(Name(ii, jj)), 'w') as H:
            H.write(s)
        with open('output/{}.qsub'.format(Name(ii, jj)), 'w') as K:
            K.write(t)

u = bashFile(dia, erg)
with open('output/aRun.sh', 'w') as Y:
    Y.write(u)