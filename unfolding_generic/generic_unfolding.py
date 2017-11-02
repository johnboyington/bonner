'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfoldingTools import BonnerSphereTools
import numpy as np
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP

unfold = BonnerSphereTools()


class GenericUnfolding(BonnerSphereTools):

    def __init__(self):
        BonnerSphereTools.__init__(self)
        self.loadBonnerResponses()
        self.loadResponseFunctionData()
        self.runExperiment()

    def loadBonnerResponses(self):
        responseData = np.loadtxt('data/bonner_data.txt')
        responseError = np.sqrt(responseData) / responseData
        extraError = np.full(responseData, 0.5)
        self.setResponseData(responseData, responseError, extraError)

    def loadResponseFunctionData(self):
        genericData = np.loadtxt('data/generic_data.txt')
        genericData = genericData.reshape(len(unfold.sphereSizes), -1, 4)
        self.edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
        responseFunctions = genericData[:, :, 2]
        self.setResponseFunctionData(self.edges, responseFunctions)

    def loadDefaultSpectrumTypical(self):
        f = FluxTypical(1./7., 600.0)
        flux = f.make_discrete(self.edges * 1E6, scaling=5E12)
        dsErr = np.full(flux.shape, 0.5)
        self.setDefaultSpectrum(self.edges, flux, dsErr)

    def loadDefaultSpectrumNEBP(self):
        f = FluxNEBP(250)
        flux = f.change_bins(self.edges)
        dsErr = np.full(flux.shape, 0.5)
        self.setDefaultSpectrum(self.edges, flux, dsErr)

    def runExperiment(self):
        # run with typical spectrum for default spectrum
        self.loadDefaultSpectrumTypical()
        self.setRoutine('gravel')
        self.run('gravel')
        self.plotSpectra()
        # run with nebp spectrum for default spectrum
        self.loadDefaultSpectrumNEBP()
        self.setRoutine('gravel')
        self.run('gravel')
        self.plotSpectra()


if __name__ == '__main__':
    unfold = GenericUnfolding()

'''
###############################################################################
# writing over the default spectrum

if False:
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
'''
