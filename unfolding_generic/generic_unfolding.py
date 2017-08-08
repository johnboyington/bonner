'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfoldingTools import BonnerSphereTools
import numpy as np

unfold = BonnerSphereTools()


# sphereIDs - a list of lists that contains an 8 character short ID and 16 char long ID for 
#             naming each sphere
unfold.sphereIDs = [['    bare', '      bareSphere'],
                    ['     2in', '       2inSphere'],
                    ['     3in', '       3inSphere'],
                    ['     5in', '       5inSphere'],
                    ['     8in', '       8inSphere'],
                    ['    10in', '      10inSphere'],
                    ['    12in', '      12inSphere']]

# sphereSizes - the sphere diameters in inches
unfold.sphereSizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]

# responseData - the measured response from each bonner sphere
unfold.responseData = np.loadtxt('bonner_data.txt')

# responseError - the uncertainty associated with responseData due to statistics (as a percentage)
unfold.responseError = np.sqrt(unfold.responseData) / unfold.responseData

# extraError - uncertainty in responseData due to causes other than statistics (as a percentage)
unfold.extraError = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# correctionFactor - a factor by which to multiply measured data and absolute uncertainties
#                    entering a value of zero means data remains unchanged
unfold.correctionFactor = 0


# read in response function data from a text file and reshape based on number of spheres and energy groups
genericData = np.loadtxt('generic_data.txt')
genericData = genericData.reshape(len(unfold.sphereSizes), -1, 4)



# rfErgEdges = the energy bin edges of the response functions
unfold.rfErgEdges = genericData[:,:,1][0]

# responses - the 2x2 matrix containing the responses for each sphere
unfold.responses = genericData[:,:,2]

# reErgUnits - the units of the response functions, either 'MeV', 'keV', or 'eV'
unfold.rfErgUnits = 'MeV'


'''
PARAMETERS ASSOCIATED WIHT THE DEFAULT SPECTRUM
mode - the default spectrum input format
    1 - (fluence rate per bin) / (width of the bin in E)     ~ dPhi / dE
    2 - fluence rate per bin
    3 - (fluence rate per bin) / (width of the bin in ln(E))     ~ E * dPhi / dE
reErgUnits - the units of the default spectrum, either 'MeV', 'keV', or 'eV'
dS - the default spectrum
dsErr - the uncertainty associated with the default spectrum
dsErgEdges - the energy bin edges of the default spectrum
'''

unfold.mode = 1
unfold.dsErgUnits = 'MeV'
unfold.dS = np.ones(len(unfold.rfErgEdges))
unfold.dsErr = np.full(unfold.dS.shape, 0.5)
unfold.dsErgEdges = genericData[:,:,1][0]



unfold.ibuName = 'generic'
unfold.fmtName = 'generic'
unfold.fluName = 'generic'
unfold.outName = 'generic'
unfold.inpName = 'generic'
unfold.finalChiSqr = 1.1
unfold.temp = [[1.0, 0.85]]
unfold.solnStructure = 2
unfold.solnRepresentation = 1
unfold.scaling = [0, 1, 1]


