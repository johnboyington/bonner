import numpy as np
import matplotlib.pyplot as plt
from nice_plots import Nice_Plots
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
from folding import Folding


class Folding_Experiment(object):

    def __init__(self):
        Nice_Plots()
        self.normalize_experimental_responses()
        self.fold_typical()
        self.fold_nebp()
        self.plot_theoretical()
        self.plot_unscaled()
        self.plot_scaled()
        self.plot_diffs()
        if False:
            print(self.experimental_responses)
            print(self.typical_response)
            print(self.nebp_response)

    def normalize_experimental_responses(self):
        s = 5 * 60  # 5 minutes
        r = np.array([141585, 102435, 76796, 38056, 13923, 8091, 4834]) / s
        powers = np.full(len(r), 250) / np.array([25.2, 25.15, 25.15, 25.13, 25.13, 25.15, 25.15])
        # efficiency_correction
        e = 1
        self.experimental_responses = r * powers * (1 / e)

    def fold_typical(self):
        # input response matrix
        genericData = np.loadtxt('nebp_response_functions.txt')
        genericData = genericData.reshape(7, -1, 4)
        edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
        rfs = genericData[:, :, 2]

        # produce spectrum object for nebp
        sf = 294858.046942 / 0.0263292381867
        f = FluxTypical(edges, sf, 1./7., 600.0)
        f.change_bins(edges)

        # create and test object
        fold = Folding()
        fold.set_spectrum(f)
        print('Typical total flux: {}'.format(fold.spectrum.total_flux))
        fold.set_response_functions(rfs)
        self.typical_response = fold.fold()

    def fold_nebp(self):
        # input response matrix
        genericData = np.loadtxt('nebp_response_functions.txt')
        genericData = genericData.reshape(7, -1, 4)
        edges = np.concatenate((np.array([1E-11]), genericData[:, :, 1][0]))
        rfs = genericData[:, :, 2]

        # produce spectrum object for nebp
        f = FluxNEBP(250)
        f.change_bins(edges)

        # create and test object
        fold = Folding()
        fold.set_spectrum(f)
        print('NEBP total flux:    {}'.format(fold.spectrum.total_flux))
        fold.set_response_functions(rfs)
        self.nebp_response = fold.fold()

    def plot_theoretical(self):
        plt.figure(50)
        plt.yscale('log')
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        plt.plot(sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.legend()
        plt.savefig('responses_no_exp.png', dpi=250)
        plt.close()

    def plot_unscaled(self):
        plt.figure(51)
        plt.yscale('log')
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        plt.plot(sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.plot(sizes, self.experimental_responses, 'ro', label='experimental (scaled *100)')
        plt.legend()
        plt.savefig('responses_unscaled_exp.png', dpi=250)
        plt.close()

    def plot_scaled(self):
        plt.figure(52)
        plt.yscale('log')
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        plt.plot(sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.plot(sizes, self.experimental_responses * 100, 'ro', label='experimental (scaled *100)')
        plt.legend()
        plt.savefig('responses_scaled_exp.png', dpi=250)
        plt.close()

    def plot_diffs(self):
        diffs = self.nebp_response - (self.experimental_responses * 100)
        plt.figure(53)
        # plt.yscale('log')
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        plt.plot(sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.plot(sizes, self.experimental_responses * 100, 'ro', label='experimental (scaled *100)')
        plt.plot(sizes, diffs, 'g^', label='difference')
        plt.legend()
        plt.savefig('responses_error.png', dpi=250)
        plt.close()


if __name__ == '__main__':
    do = Folding_Experiment()
