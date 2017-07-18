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

import bonner_functions as bonner
import time
start_time = time.time()


#hard code groups
sphere_diameters = [2, 3, 5, 8, 10, 12] #[0, 2, 3, 5, 8, 10, 12]
energy_groups = [                     4.00000000e-09,   1.00000000e-08,   2.53000000e-08,
                    4.00000000e-08,   5.00000000e-08,   6.00000000e-08,   8.00000000e-08,
                    1.00000000e-07,   1.50000000e-07,   2.00000000e-07,   2.50000000e-07,
                    3.25000000e-07,   3.50000000e-07,   3.75000000e-07,   4.50000000e-07,
                    6.25000000e-07,   1.01000000e-06,   1.08000000e-06,   1.13000000e-06,
                    5.00000000e-06,   6.25000000e-06,   6.50000000e-06,   6.88000000e-06,
                    7.00000000e-06,   2.05000000e-05,   2.12000000e-05,   2.18000000e-05,
                    3.60000000e-05,   3.71000000e-05,   6.50000000e-05,   6.75000000e-05,
                    1.01000000e-04,   1.05000000e-04,   1.16000000e-04,   1.18000000e-04,
                    1.88000000e-04,   1.92000000e-04,   2.25000000e-03,   3.74000000e-03,
                    1.70000000e-02,   2.00000000e-02,   5.00000000e-02,   2.00000000e-01,
                    2.70000000e-01,   3.30000000e-01,   4.70000000e-01,   6.00000000e-01,
                    7.50000000e-01,   8.61000000e-01,   1.20000000e+00,   1.50000000e+00,
                    1.85000000e+00,   3.00000000e+00,   4.30000000e+00,   6.43000000e+00,
                    2.00000000e+01]

                    
fast_energy_groups = [1.00000000e-07,   1.50000000e-07,   2.00000000e-07,   2.50000000e-07,
                    3.25000000e-07,   3.50000000e-07,   3.75000000e-07,   4.50000000e-07,
                    6.25000000e-07,   1.01000000e-06,   1.08000000e-06,   1.13000000e-06,
                    5.00000000e-06,   6.25000000e-06,   6.50000000e-06,   6.88000000e-06,
                    7.00000000e-06,   2.05000000e-05,   2.12000000e-05,   2.18000000e-05,
                    3.60000000e-05,   3.71000000e-05,   6.50000000e-05,   6.75000000e-05,
                    1.01000000e-04,   1.05000000e-04,   1.16000000e-04,   1.18000000e-04,
                    1.88000000e-04,   1.92000000e-04,   2.25000000e-03,   3.74000000e-03,
                    1.70000000e-02,   2.00000000e-02,   5.00000000e-02,   2.00000000e-01,
                    2.70000000e-01,   3.30000000e-01,   4.70000000e-01,   6.00000000e-01,
                    7.50000000e-01,   8.61000000e-01,   1.20000000e+00,   1.50000000e+00,
                    1.85000000e+00,   3.00000000e+00,   4.30000000e+00,   6.43000000e+00,
                    2.00000000e+01]

for sphere in sphere_diameters:
    for energy in fast_energy_groups:
        bonner.runFile2(sphere, energy)


print('Script Complete in {} seconds.'.format(time.time() - start_time))
