'''
Bonner Sphere Functions
Initialized 6/22/17 by John Boyington

This code contains the functions used in the other bonner response generators
in this repository.
'''

import numpy as np




def mcnpWriter(size, energy):
    s = ''
    s += open('card0.txt', 'r').read()
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
    with open('output/bonnerSphere.i', 'w') as F:
        F.write(s)
    return

def advantgWriter():
    return

sphere_diameter = 1 * 2.54
energy = 1E-2
mcnpWriter(sphere_diameter, energy)