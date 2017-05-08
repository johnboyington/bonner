#this code will write the mcnp6 input files used to find the Bonner Sphere response
#functions

import numpy as np
import matplotlib.pyplot as plt
import os

try:
    os.mkdir('/home/john/bonner_sphere/mcnp/writer/output')
except OSError,e:
    print e


rawdata = np.array([1935, 8823, 11049, 6825, 2544, 1402, 896])

sizeinch = np.array([0, 2, 3, 5, 8, 10, 12])
size = (sizeinch * 2.54) / 2.

#these bins aren't quite right
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

eb = eq[::-1]

cb = np.array([180, 90, 80, 70, 60, 50, 40, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
cbw = cb[:-1] - cb[1:]
cbr = cb[::-1]
f = np.pi / 180.
ab = np.cos(cb * f)

ndata = np.loadtxt('ndata.txt')[:,1:].T
nfl = ndata[0].reshape(len(cbw),-1).T
netot = np.sum(nfl, axis=1)

def Source(numb, ee, eee):
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

def Sphere(big):
    H = ''
    H = '01  S   0 0 -0.9  {}    $Bonner Sphere\n'.format(big)
    return H

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
def Name(big, erg):
    N = 's{}e{}'.format(big, erg)
    return N

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
    
#set parameters
erg = np.array(range(len(eb) - 9)) + 1
dia = range(len(size))

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
        with open('/home/john/bonner_sphere/mcnp/writer/output/{}.i'.format(Name(ii, jj)), 'w') as H:
            H.write(s)
        with open('/home/john/bonner_sphere/mcnp/writer/output/{}.qsub'.format(Name(ii, jj)), 'w') as K:
            K.write(t)


