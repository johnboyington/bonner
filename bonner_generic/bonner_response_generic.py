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

t = time.time()
response = []

sphere_diameter = 12 
sphere_diameter *= (2.54 / 2)
energy = 1E1 #MeV


bonner.mcnpWriter(sphere_diameter, energy)
response.append(bonner.runFile())

print response
print 'Script Complete in {} seconds.'.format(time.time() - t)