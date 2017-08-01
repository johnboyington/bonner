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
sphere_diameters = [0, 2, 3, 5, 8, 10, 12]

                    
decker_energy_groups = [1.0000E-08, 2.5120E-08, 6.3100E-08, 1.0000E-07, 
                        2.5120E-07, 1.0000E-06, 1.0000E-05, 1.0000E-04, 
                        1.0000E-03, 1.0000E-02, 2.5120E-02, 3.9810E-02, 
                        6.3100E-02, 1.0000E-01, 1.5850E-01, 2.5120E-01, 
                        3.9810E-01, 6.3100E-01, 1.0000E+00, 1.5850E+00, 
                        2.5120E+00, 3.9810E+00, 6.3100E+00, 1.0000E+01, 
                        1.5850E+01, 2.5120E+01]

sphere_diameters = [5]
decker_energy_groups = [6.3100E-01]

desired_error_max = 0.05
initial_nps = 1000000

for sphere in sphere_diameters:
    for energy in decker_energy_groups:
        print('***********************************************************')
        print('NEW SPHERE Diameter {} in. Energy {:e} MeV written.'.format(sphere, energy))
        print('***********************************************************')
        nps_old = int(initial_nps)
        response = bonner.imp_spheres_mcnpWriter(sphere, energy, initial_nps)
#        with open('output/response_data.txt', 'a+') as File:
#            File.write('{:2}   {:14.8e}   {:14.8e}   {:14.8e} \n'.format(sphere, energy, response[0], response[1]))


print('Script Complete in {} seconds.'.format(time.time() - start_time))
