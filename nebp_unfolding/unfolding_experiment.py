'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfolding_tools import Unfolding
import numpy as np
from spectrum import Spectrum
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
import shutil


class Experiment(object):

    def __init__(self):
        self.load_data()
        self.run_all()

    def load_responses(self):
        print('Loading Detector Response Data...')
        bg = np.loadtxt('bonner_data_bg.txt', skiprows=1)

        s = 5 * 60  # 5 minutes
        r = np.loadtxt('bonner_data.txt', skiprows=1)
        r -= bg
        powers = np.full(len(r), 250) / np.array([25.2, 25.15, 25.15, 25.13, 25.13, 25.15, 25.15])
        # efficiency_correction
        e = 1
        self.experimental_response = r * powers * (1 / e) * (1 / s)

        # load 2nd dataset
        s = 5 * 60  # 5 minutes
        r = np.loadtxt('bonner_data2.txt', skiprows=1)
        r -= bg
        powers = (250 / 24.86)
        # efficiency_correction
        e = 1
        self.experimental_response2 = r * powers * (1 / e) * (1 / s)

        # load 3rd (filtered) dataset
        s = 5 * 60  # 5 minutes
        r = np.loadtxt('bonner_data3.txt', skiprows=1)
        r -= bg
        powers = (250 / 24.86)
        # efficiency_correction
        e = 1
        self.experimental_response3 = r * powers * (1 / e) * (1 / s)
        print('    Experimental Response Data Loaded')
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

    def load_data(self):
        self.load_responses()
        self.load_response_functions()
        self.load_typical_spectrum()
        self.load_nebp_spectrum()
        self.load_filtered_spectrum()

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
        print('\n')
        print('Running First Experimental Responses, NEBP Spectrum...')
        self.run_set(self.experimental_response, self.nebp_spectrum, 'ex_ne')

        print('Running Second Experimental Responses, NEBP Spectrum...')
        self.run_set(self.experimental_response2, self.nebp_spectrum, 'e2_ne')

        print('Running Third Experimental Responses, NEBP Spectrum...')
        self.run_set(self.experimental_response3, self.nebp_spectrum, 'e3_ne')

        print('Running Third Experimental Responses, Filtered NEBP Spectrum...')
        self.run_set(self.experimental_response3, self.filtered_spectrum, 'e3_fi')

        print('Running Theoretical Responses, NEBP Spectrum...')
        self.run_set(self.theoretical_response, self.nebp_spectrum, 'th_ne')

        print('Running Theoretical Responses, Typical LWR Spectrum...')
        self.run_set(self.theoretical_response, self.nebp_spectrum, 'th_ty')

        print('Finished Unfolding\n')
        shutil.rmtree('inp')
