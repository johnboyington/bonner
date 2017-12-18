'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfolding_tools import Unfolding
import numpy as np
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
import shutil


class Experiment(object):

    def __init__(self):
        self.load_data()
        self.run_all()

    def load_responses(self):
        print('Loading Detector Response Data...')
        self.experimental_response = np.loadtxt('bonner_data.txt')
        # used in unfolding but I want to move these to the unfolding class -
        #  responseError = np.sqrt(self.experimental_response) / responseData
        #  extraError = np.full(len(self.experimental_response), 0.5)
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

    def load_data(self):
        self.load_responses()
        self.load_response_functions()
        self.load_typical_spectrum()
        self.load_nebp_spectrum()

    def run_experiment_ex_ne(self):
        # run with nebp spectrum for with experimental data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(self.experimental_response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(self.nebp_spectrum)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('ex_ne_gr')
        self.unfolding.run('ex_ne_gr')
        self.unfolding.set_routine('maxed')
        self.unfolding.set_names('ex_ne_mx')
        self.unfolding.run('ex_ne_mx')

    def run_experiment_ex_ty(self):
        # run with typical spectrum for with experimental data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(self.experimental_response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(self.typical_spectrum)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('ex_ty_gr')
        self.unfolding.run('ex_ty_gr')
        self.unfolding.set_routine('maxed')
        self.unfolding.set_names('ex_ty_mx')
        self.unfolding.run('ex_ty_mx')

    def run_experiment_th_ne(self):
        # run with nebp spectrum for with theoretical data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(self.theoretical_response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(self.nebp_spectrum)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('th_ne_gr')
        self.unfolding.run('th_ne_gr')
        self.unfolding.set_routine('maxed')
        self.unfolding.set_names('th_ne_mx')
        self.unfolding.run('th_ne_mx')

    def run_experiment_th_ty(self):
        # run with typical spectrum for with theoretical data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(self.theoretical_response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(self.typical_spectrum)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('th_ty_gr')
        self.unfolding.run('th_ty_gr')
        self.unfolding.set_routine('maxed')
        self.unfolding.set_names('th_ty_mx')
        self.unfolding.run('th_ty_mx')

    def run_all(self):
        print('\n')
        print('Running Experimental Responses, NEBP Spectrum...')
        self.run_experiment_ex_ne()
        print('Running Experimental Responses, Typical LWR Spectrum...')
        self.run_experiment_ex_ty()
        print('Running Theoretical Responses, NEBP Spectrum...')
        self.run_experiment_th_ne()
        print('Running Theoretical Responses, Typical LWR Spectrum...')
        self.run_experiment_th_ty()
        print('Finished Unfolding')
        shutil.rmtree('inp')
