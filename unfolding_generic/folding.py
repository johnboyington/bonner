import numpy as np
import matplotlib.pyplot as plt
from nebp_spectrum import FluxNEBP
from spectrum import Spectrum


class Folding(object):

    def __init__(self, sf=1, sizes=False):
        self.set_scaling_factor(sf)
        self.set_sphere_sizes(sizes)
        self.solutions = []

    def set_spectrum(self, spectrum):
        self.spectrum = spectrum

    def set_response_functions(self, matrix):
        self.response_matrix = matrix

    def set_scaling_factor(self, sf):
        self.scaling_factor = sf

    def set_sphere_sizes(self, sizes):
        if not sizes:
            self.sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        else:
            self.sizes = sizes

    def fold(self):
        detector_responses = []
        for f in self.response_matrix:
            detector_responses.append(np.sum(self.spectrum.values * f) * self.scaling_factor)
        self.append_solution(detector_responses)

    def plot(self):
        styles = ['ko', 'ro', 'kx']
        plt.figure(0)
        for i, sol in enumerate(self.solutions):
            plt.plot(self.sizes, sol, styles[i])
        plt.yscale('log')
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        plt.savefig('responses.png')

    def append_solution(self, sol):
        self.solutions.append(sol)

    def run_all(self):
        pass


if __name__ == '__main__':
    # input response matrix
    genericData = np.loadtxt('data/generic_data.txt')
    genericData = genericData.reshape(7, -1, 4)
    edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
    rfs = genericData[:, :, 2]

    # produce spectrum object for nebp
    f = FluxNEBP(250)
    flux = f.change_bins(edges)
    dsErr = np.full(len(flux), 0.5)
    s = Spectrum(np.array([edges, flux, dsErr]).T)
    print(f.values)
    print(rfs[0])

    # create and test object
    fold = Folding()
    fold.set_spectrum(f)
    fold.set_response_functions(rfs)
    fold.fold()
    fold.append_solution([141585, 102435, 76796, 38056, 13923, 8091, 4834])
    fold.plot()
