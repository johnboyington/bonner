'''
Bonner Sphere Functions
Initialized 6/22/17 by John Boyington

This code contains the functions used in the other bonner response generators
in this repository.
'''

import os
import shutil
import time
import subprocess
import psutil
import signal



def mcnpWriter(size, energy, particles=100000):
    s = open('card0.txt', 'r').read()
    s += '01  S   0 0 -0.9  {}    $Bonner Sphere\n'.format(size)
    s += open('card1.txt', 'r').read()
    s += 'NPS   {}\n'.format(particles)
    s += 'c  ---------------------------------------------------------\n'
    s += 'c                    SOURCE SPECIFICATIONS\n'
    s += 'c  ---------------------------------------------------------\n'
    s += 'SDEF   POS=-15.24 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG={}\n'.format(energy)
    s += '       DIR=1 RAD=D6 PAR=1\n'
    s += 'SI6   0  {}\n'.format(size)
    s += 'SP6 -21  1\n'
    s += open('card2.txt', 'r').read()
    with open('working/inp', 'w') as F:
        F.write(s)
    print('Sphere Diameter {} in. Energy {:e} MeV written.'.format((size * 2) / 2.54, energy))
    return


def advantgWriter(size, voxel):
    
    s = open('template.adv', 'r').read()
    s += 'mesh_x                     -40 -{} {} 20\n'.format(size, size)
    s += 'mesh_y                     -20 -{} {} 20\n'.format(size, size)
    s += 'mesh_z                     -40 -{} {} 30\n'.format(size, size)
    s += 'mesh_x_ints                {} {} {}\n'.format(1, int(round((1 / voxel) * size * 2)), 1)
    s += 'mesh_y_ints                {} {} {}\n'.format(1, int(round((1 / voxel) * size * 2)), 1)
    s += 'mesh_z_ints                {} {} {}\n'.format(1, int(round((1 / voxel) * size * 2)), 1)
    with open('working/bonnerSphere.adv', 'w') as F:
        F.write(s)
    return



def Extract():
    F = open('outp', 'r').readlines()
    for ii in range(len(F)):
        if ' multiplier bin:   1.00000E+00         2         105' in F[ii]:
            line = F[ii + 1]
            val = float(line[17:28])
            err = float(line[29:35])
            return [val, err]



def runFile():
    os.chdir('working')
    os.system('mcnp6 inp=inp tasks 27')
    response = Extract()
    if response[2] == 0 or response[2] > 0.05:
        print('Error above threshold. Invoking Advantg')
        os.system('advantg bonnerSphere.adv')
        os.chdir('output')
        os.system('mcnp6 inp=inp wwinp=wwinp tasks 27')
        response = Extract()
        os.chdir('..')
        shutil.rmtree('adj_solution')
        shutil.rmtree('model')
        shutil.rmtree('output')
    os.remove('inp')
    os.remove('outp')
    os.remove('runtpe')
    os.chdir('..')
    return response




def runFile2(size, energy):
    mcnpWriter(size * (2.54 / 2), energy)
    advantgWriter(size * (2.54 / 2))
    os.chdir('working')
    os.system('mcnp6 inp=inp tasks 27')
    response = Extract()
    if response[1] == 0 or response[1] > 0.05:
        print('Error above threshold. Invoking Advantg')
        os.system('advantg bonnerSphere.adv')
        os.chdir('output')
        os.system('mcnp6 inp=inp wwinp=wwinp tasks 27')
        response = Extract()
        os.chdir('..')
        shutil.rmtree('adj_solution')
        shutil.rmtree('model')
        shutil.rmtree('output')
    os.remove('inp')
    os.remove('outp')
    os.remove('runtpe')
    os.chdir('..')
    with open('output/response_data.txt', 'a') as File:
        File.append('{:2d}   {:14.8e}   {:14.8e}   {:14.8e} \n'.format(size, energy, response[0], response[1]))
    return



def timedMCNP(max_runtime):
    mcnp_start_time = time.time()
    TIMEOUT = max_runtime
    subp = subprocess.Popen(['mcnp6', 'inp=inp', 'wwinp=wwinp', 'tasks 26'], shell=False)
    p = psutil.Process(subp.pid)
    while p.is_running():
        if (time.time() - mcnp_start_time) > TIMEOUT:
            os.kill(subp.pid, 0)
            response = [0, 0]
            return response
        time.sleep(5)
    return


def runAdvComp():
    adv_start_time = time.time()
    os.chdir('working')
    os.system('advantg bonnerSphere.adv')
    adv_time = adv_start_time - time.time()
    os.chdir('output')
    mcnp_start_time = time.time()
    TIMEOUT = 20
    mcnp_time = mcnp_start_time - time.time()
    response = timedMCNP(TIMEOUT)
    if response != [0, 0]:
        response = Extract()
    os.chdir('..')
    shutil.rmtree('adj_solution')
    shutil.rmtree('model')
    shutil.rmtree('output')
    os.remove('inp')
    os.chdir('..')
    return response, adv_time, mcnp_time
