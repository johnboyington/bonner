'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfolding_tools import Unfolding
import numpy as np
from spectrum import Spectrum
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
import experimental_data
import shutil


class Experiment(object):

    def __init__(self):
        self.load_data()
        self.run_all()

    def load_responses(self):
        self.theoretical_response = np.loadtxt('nebp_theoretical_response.txt')
        print('    Theoretical Response Data Loaded\n')

    def load_response_functions(self):
        print('Loading Response Function Data...')
        data = np.loadtxt('nebp_response_functions.txt')
        data = data.reshape(7, -1, 4)
        self.edges = np.concatenate((np.array([1E-11]), data[:, :, 1][0]))
        self.c = 1.774E-2 * (1/4)  # the scaling factor for the response functions
        self.rf = data[:, :, 2] * self.c
        print('    Response Function Data Loaded\n')

    def load_typical_spectrum(self):
        print('Loading Typical LWR Spectrum...')
        sf = 294858.046942 / 0.0263292381867
        self.typical_spectrum = FluxTypical(self.edges, sf, 1./7., 600.0)
        self.typical_spectrum.change_bins(self.edges)
        print('    Typical LWR Spectrum Loaded\n')

    def load_nebp_spectrum(self):
        print('Loading NEBP Spectrum...')
        self.nebp_spectrum = FluxNEBP(250)
        print('    NEBP Spectrum Loaded\n')

    def load_filtered_spectrum(self):
        print('Loading Filtered Spectrum...')
        bins = np.loadtxt('scale56.txt')
        # calculate neutron scaling factor
        tally_area = tally_area = np.pi * (1.27 ** 2)
        cn = 2.54 / (200 * 1.60218e-13 * tally_area)
        cn *= 7.53942E-8
        cn *= 250  # normalize to 250 W(th)
        n_fil = np.loadtxt('n_fil2.txt')
        n_fil = n_fil.T[1][1:] * cn
        self.filtered_spectrum = Spectrum(bins, n_fil)
        print('    Filtered Spectrum Loaded\n')

    def load_unity_spectrum(self):
        print('Loading Unity Spectrum...')
        bins = np.loadtxt('scale56.txt')
        ones = np.ones(len(bins) - 1)
        self.unity_spectrum = Spectrum(bins, ones, dfde=True)
        print('    Unity Spectrum Loaded\n')

    def load_data(self):
        self.load_responses()
        self.load_response_functions()
        self.load_typical_spectrum()
        self.load_nebp_spectrum()
        self.load_filtered_spectrum()
        self.load_unity_spectrum()

    def run_set(self, response, ds, name):
        # run with a given set of data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(ds)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('{}_gr'.format(name))
        self.unfolding.run('{}_gr'.format(name))
        self.unfolding.set_routine('maxed')
        self.unfolding.set_names('{}_mx'.format(name))
        self.unfolding.run('{}_mx'.format(name))

    def run_all(self):
        print('\nUnfolding... \n')
        # unfolding with the first set of unfiltered responses
        self.run_set(experimental_data.unfiltered1.values, self.nebp_spectrum, 'e1_ne')

        # unfolding with the second set of unfiltered responses
        self.run_set(experimental_data.unfiltered2.values, self.nebp_spectrum, 'e2_ne')

        # unfolding with the first set of filtered responses
        self.run_set(experimental_data.filtered2.values, self.nebp_spectrum, 'f2_ne')
        self.run_set(experimental_data.filtered2.values, self.filtered_spectrum, 'f2_fi')
        self.run_set(experimental_data.filtered2.values, self.unity_spectrum, 'f2_un')

        # unfolding with the second set of filtered responses
        self.run_set(experimental_data.filtered3.values, self.nebp_spectrum, 'f3_ne')
        self.run_set(experimental_data.filtered3.values, self.filtered_spectrum, 'f3_fi')
        self.run_set(experimental_data.filtered3.values, self.unity_spectrum, 'f3_un')

        # unfolding with the theoretical response
        self.run_set(self.theoretical_response, self.nebp_spectrum, 'th_ne')

        print('Finished Unfolding\n')
        shutil.rmtree('inp')
