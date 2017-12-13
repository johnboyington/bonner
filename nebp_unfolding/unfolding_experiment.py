'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfolding_tools import Unfolding
import numpy as np
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
from spectrum import Spectrum


class Experiment(object):

    def __init__(self):
        self.load_data()
        self.run_all()

    def load_responses(self):
        print('Loading Detector Response Data...')
        responseData = np.loadtxt('bonner_data.txt')
        responseError = np.sqrt(responseData) / responseData
        extraError = np.full(len(responseData), 0.5)
        print('Experimental Response Data Loaded')
        if False:
            print('Theoretical Response Data Loaded')

    def load_response_functions(self):
        print('Loading Response Function Data...')
        data = np.loadtxt('nebp_response_functions.txt')
        data = data.reshape(7, -1, 4)
        self.edges = np.concatenate((np.array([1E-11]), data[:, :, 1][0]))
        self.rf = data[:, :, 2]
        print('Response Function Data Loaded')

    def load_typical_spectrum(self):
        print('Loading Typical LWR Spectrum...')
        sf = 294858.046942 / 0.0263292381867
        self.typical_spectrum = FluxTypical(self.edges, sf, 1./7., 600.0).change_bins(self.edges)
        print('Typical LWR Spectrum Loaded')

    def load_nebp_spectrum(self):
        print('Loading NEBP Spectrum...')
        self.nebp_spectrum = FluxNEBP(250).change_bins(self.edges)
        print('NEBP Spectrum Loaded')
    
    def load_data(self):
        self.load_responses()
        self.load_response_functions()
        self.load_typical_spectrum()
        self.load_nebp_spectrum()

    def run_experiment(self):
        # run with typical spectrum for default spectrum
        self.unfolding = Unfolding()
        self.loadDefaultSpectrumTypical()
        self.setRoutine('gravel')
        self.run('gravel_typical')
        self.setRoutine('maxed')
        self.run('maxed_typical')
        self.plotSpectra(name='typical')
    
    def run_all(self):
        pass


if __name__ == '__main__':
    unfold = GenericUnfolding()

