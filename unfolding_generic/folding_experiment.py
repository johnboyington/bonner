import numpy as np
import matplotlib.pyplot as plt
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
from spectrum import Spectrum
from folding import Folding


class Folding_Experiment(object):

    def __init__(self):
        self.experimental_responses = [141585, 102435, 76796, 38056, 13923, 8091, 4834]
        self.fold_typical()
        self.fold_nebp()

    def fold_typical(self):
        # input response matrix
        genericData = np.loadtxt('data/generic_data.txt')
        genericData = genericData.reshape(7, -1, 4)
        edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
        rfs = genericData[:, :, 2]

        # produce spectrum object for nebp
        f = FluxTypical(edges, 1, 1./7., 600.0)
        print(f.total_flux)

        # create and test object
        fold = Folding()
        fold.set_spectrum(f)
        fold.set_response_functions(rfs)
        self.typical_response = fold.fold()

    def fold_nebp(self):
        # input response matrix
        genericData = np.loadtxt('data/generic_data.txt')
        genericData = genericData.reshape(7, -1, 4)
        edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
        rfs = genericData[:, :, 2]

        # produce spectrum object for nebp
        f = FluxNEBP(250)
        f.change_bins(edges)
        print(f.total_flux)

        # create and test object
        fold = Folding()
        fold.set_spectrum(f)
        fold.set_response_functions(rfs)
        self.nebp_response = fold.fold()

    def make_plot(self):
        pass

if __name__ == '__main__':
    do = Folding_Experiment()
