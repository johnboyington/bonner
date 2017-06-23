'''
Bonner Sphere Functions
Initialized 6/22/17 by John Boyington

This code contains the functions used in the other bonner response generators
in this repository.
'''

import numpy as np
import os
import shutil



def mcnpWriter(size, energy):
    s = open('card0.txt', 'r').read()
    s += '01  S   0 0 -0.9  {}    $Bonner Sphere\n'.format(size)
    s += open('card1.txt', 'r').read()
    s += 'c  ---------------------------------------------------------\n'
    s += 'c                    SOURCE SPECIFICATIONS\n'
    s += 'c  ---------------------------------------------------------\n'
    s += 'SDEF   POS=-15.24 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG={}\n'.format(energy)
    s += '       DIR=1 RAD=D6 PAR=1\n'
    s += 'SI6   0  1.27\n'.format(size)
    s += 'SP6 -21  1\n'
    s += open('card2.txt', 'r').read()
    with open('working/inp', 'w') as F:
        F.write(s)
    print 'Sphere Diameter {} in. Energy {:e} MeV written.'.format((size * 2) / 2.54, energy)
    return


def Extract():
    F = open('outp', 'r').readlines()
    for ii in range(len(F)):
        if ' multiplier bin:   1.00000E+00         4         105' in F[ii]:
            line = F[ii + 1]
            val = float(line[17:28])
            err = float(line[29:35])
            return [val, err * val, err]



def runFile():
    os.chdir('working')
    os.system('mcnp6 inp=inp tasks 28')
    response = Extract()
    if response[2] == 0 or response[2] > 0.05:
        print 'Error above threshold. Invoking Advantg'
        os.system('advantg bonnerSphere.adv')
        os.chdir('output')
        os.system('mcnp6 inp=inp wwinp=wwinp tasks 28')
        response = Extract()
        os.chdir('..')
    os.remove('inp')
    os.remove('outp')
    os.remove('runtpe')
    shutil.rmtree('adj_solution')
    shutil.rmtree('model')
    shutil.rmtree('output')
    os.chdir('..')
    return response


