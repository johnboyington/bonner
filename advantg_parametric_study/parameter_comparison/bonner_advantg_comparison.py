'''
Bonner Sphere Generic Response Generator
Initialized 6/22/17 by John Boyington


This code is meant to reproduce response functions similar to that found in:
DECKER et al.: NOVEL BONNER SPHERE SPECTROMETER RESPONSE FUNCTIONS USING MCNP6

Inputs
    - Energy Bin Structure
    - Bonner Sphere Sizes

Functionality
    - Creates Advantg and mcnp inputs
    - Runs Advantg
    - Runs mcnp with advantg ww's
    - Extracts response values from mcnp output file
    - Deletes advantg and mcnp files
    - Normalizes Response Functions

Outputs
    - Plots of the Responses
    - MaxED Input file
    - Text file with Response Values
'''

import matplotlib.pyplot as plt
import numpy as np
import bonner_functions as bonner
import os
import time
start_time = time.time()



                    

test_files = [(5, 6.00000000e-08), (5, 6.50000000e-05)]
voxel_sizes = [0.5, 1]

for case in test_files:
    for voxel in voxel_sizes:
        bonner.mcnpWriter(case[0] * (2.54 / 2), case[1])
        bonner.advantgWriter(case[0] * (2.54 / 2), voxel)
        response = bonner.runAdvComp()
        with open('output/response_data.txt', 'a') as F:
            F.append('{:2d}   {:14.8e}   {:4.3f}   {:14.8e}   {:14.8e}   {:14.8e}   {:14.8e} \n'
                        .format(case[0], case[1], voxel, response[0], response[1], response[2], response[3]))


print('Script Complete in {} seconds.'.format(time.time() - start_time))
