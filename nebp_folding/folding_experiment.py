import numpy as np
import matplotlib.pyplot as plt
from nice_plots import Nice_Plots
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
from folding import Folding


class Folding_Experiment(object):

    def __init__(self, plot_all=False):
        Nice_Plots()
        self.set_coefficient()
        self.sizes = [0.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0]
        self.get_robert_data()
        self.normalize_experimental_responses()
        self.fold_typical()
        self.fold_nebp()
        self.plot_responses()
        if plot_all:
            self.plot_theoretical()
            self.plot_diffs()
            self.plot_robert()

    def set_coefficient(self):
        self.c = 1.774E-2 * (1/4)

    def normalize_experimental_responses(self):
        s = 5 * 60  # 5 minutes
        r = np.array([141585, 102435, 76796, 38056, 13923, 8091, 4834]) / s
        powers = np.full(len(r), 250) / np.array([25.2, 25.15, 25.15, 25.13, 25.13, 25.15, 25.15])
        # efficiency_correction
        e = 1
        self.experimental_responses = r * powers * (1 / e)

    def get_robert_data(self):
        self.robert_responses = np.array([1935, 8823, 11049, 6825, 2544, 1402, 896]) * 0.18

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
        fold = Folding(sf=self.c)
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
        fold = Folding(sf=self.c)
        fold.set_spectrum(f)
        print('NEBP total flux:    {}'.format(fold.spectrum.total_flux))
        fold.set_response_functions(rfs)
        self.nebp_response = fold.fold()

        # store data
        s = ''
        for r in self.nebp_response:
            s += '{}\n'.format(r)
        with open('nebp_theoretical_response.txt', 'w+') as F:
            F.write(s)

    def plot_theoretical(self):
        plt.figure(50)
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        plt.plot(self.sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(self.sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.legend()
        plt.savefig('responses_theoretical.png', dpi=250)
        plt.close()

    def plot_responses(self):
        plt.figure(51)
        plt.ylabel('response $s^{-1}$')
        plt.xlabel('sphere size $in$')
        plt.plot(self.sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(self.sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.plot(self.sizes, self.experimental_responses, 'ro', label='experimental')
        plt.legend()
        plt.savefig('responses_comparison.png', dpi=250)
        plt.close()

    def plot_diffs(self):
        diffs = abs(100 * (self.experimental_responses - self.nebp_response) / self.experimental_responses)
        plt.figure(52)
        plt.ylabel('relative percent error')
        plt.xlabel('sphere size $in$')
        plt.plot(self.sizes, diffs, 'g^', label='difference')
        plt.legend()
        plt.savefig('responses_error.png', dpi=250)
        plt.close()

    def plot_robert(self):
        plt.figure(53)
        plt.ylabel('relative percent error')
        plt.xlabel('sphere size $in$')
        plt.plot(self.sizes, self.typical_response, 'kx', label='theoretical typical')
        plt.plot(self.sizes, self.nebp_response, 'ko', label='theoretical nebp')
        plt.plot(self.sizes, self.experimental_responses, 'ro', label='experimental')
        plt.plot(self.sizes, self.robert_responses, 'bo', label='robert experiment')
        plt.legend()
        plt.savefig('responses_robert.png', dpi=250)
        plt.close()


if __name__ == '__main__':
    do = Folding_Experiment(plot_all=True)
