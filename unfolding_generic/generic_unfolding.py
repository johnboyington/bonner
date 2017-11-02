'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfoldingTools import BonnerSphereTools
import numpy as np
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP

unfold = BonnerSphereTools()


# responseData - the measured response from each bonner sphere
unfold.responseData = np.loadtxt('data/bonner_data.txt')

# responseError - the uncertainty associated with responseData due to statistics (as a percentage)
unfold.responseError = np.sqrt(unfold.responseData) / unfold.responseData

# extraError - uncertainty in responseData due to causes other than statistics (as a percentage)
unfold.extraError = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]


# read in response function data from a text file and reshape based on number of spheres and energy groups
genericData = np.loadtxt('data/generic_data.txt')
genericData = genericData.reshape(len(unfold.sphereSizes), -1, 4)


# rfErgEdges = the energy bin edges of the response functions
edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
unfold.rfErgEdges = edges

# responses - the 2x2 matrix containing the responses for each sphere
unfold.responses = genericData[:, :, 2]


'''
PARAMETERS ASSOCIATED WIHT THE DEFAULT SPECTRUM
dS - the default spectrum
dsErr - the uncertainty associated with the default spectrum
dsErgEdges - the energy bin edges of the default spectrum
'''

unfold.dS = np.ones(len(unfold.rfErgEdges))
unfold.dsErr = np.full(unfold.dS.shape, 0.5)
unfold.dsErgEdges = edges


###############################################################################
# writing over the default spectrum

if True:
    f = FluxTypical(1./7., 600.0)
    flux = f.make_discrete(edges * 1E6, scaling=5E12)
    unfold.dS = flux

    # unfold.run('maxed')
    unfold.routine = 'gravel'
    unfold.run('gravel')
    unfold.plotSpectra()

if False:
    f = FluxNEBP(250)
    flux = f.change_bins(edges)
    unfold.dS = flux

    # unfold.run('maxed')
    unfold.routine = 'gravel'
    unfold.run('gravel')
    unfold.plotSpectra()
