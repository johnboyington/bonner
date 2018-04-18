from unfolding_tools import Unfolding
from nebp_spectrum import FluxNEBP
from spectrum import Spectrum
import experimental_data
import numpy as np
import shutil
from scipy.stats import norm
from numpy.random import rand


class Uncertainty_Analysis(object):
    def __init__(self):
        self.load_nebp_spectrum()
        self.load_response_functions()
        self.loop(10)

    def load_nebp_spectrum(self):
        self.nebp_spectrum = FluxNEBP(250)

    def load_response_functions(self):
        data = np.loadtxt('nebp_response_functions.txt')
        data = data.reshape(7, -1, 4)
        self.edges = np.concatenate((np.array([1E-11]), data[:, :, 1][0]))
        self.c = 1.774E-2 * (1/4)  # the scaling factor for the response functions
        self.rf = data[:, :, 2] * self.c

    def run_gravel(self, response, ds, name):
        # run with a given set of data
        self.unfolding = Unfolding()
        self.unfolding.set_responses(response)
        self.unfolding.set_rf(self.edges, self.rf)
        self.unfolding.set_ds(ds)
        self.unfolding.set_routine('gravel')
        self.unfolding.set_names('{}_gr'.format(name))
        self.unfolding.run('{}_gr'.format(name))

    def run_case(self):
        self.run_gravel(self.sample(), self.nebp_spectrum, 'er_an')
        shutil.rmtree('inp')
        data = np.loadtxt('data/{}_unfolded.txt'.format('er_an_gr'))
        data = data.T
        return Spectrum(self.edges, data[1], data[2], dfde=True)

    def sample(self):
        l = len(experimental_data.unfiltered1.values)
        sampled_response = np.zeros(l)
        for i in range(l):
            resp = experimental_data.unfiltered1.values[i]
            err = experimental_data.unfiltered1.error[i]
            fun = norm(loc=resp, scale=err)
            rho = rand()
            sampled_response[i] = fun.ppf(rho)
        return sampled_response

    def loop(self, n):
        tally = np.zeros(self.nebp_spectrum.num_bins)
        error = np.zeros(self.nebp_spectrum.num_bins)
        for i in range(n):
            spec = self.run_case()
            tally += spec.values / n
        print(tally)
            
            
        

if __name__ == '__main__':
    Uncertainty_Analysis()
