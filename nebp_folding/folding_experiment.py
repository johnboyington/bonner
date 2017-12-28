import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP
from folding import Folding


class Folding_Experiment(object):

    def __init__(self):
        self.nice_plots()
        self.set_coefficient()
        self.sizes = [0, 2, 3, 5, 8, 10, 12]
        self.get_robert_data()
        self.normalize_experimental_responses()
        self.fold_typical()
        self.fold_nebp()
        self.plot_responses()
        self.plot_theoretical()
        self.plot_diffs()
        # self.plot_robert()

    def nice_plots(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 15
        rcParams.update({'figure.autolayout': True})

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
        fig = plt.figure(50)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Response $s^{-1}$')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'green', 'marker': '^', 'markerfacecolor': 'None',
                 'markeredgecolor': 'green', 'linestyle': 'None', 'label': 'Theoretical Typical',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.typical_response, **style)
        style = {'color': 'blue', 'marker': 'o', 'markerfacecolor': 'None',
                 'markeredgecolor': 'blue', 'linestyle': 'None', 'label': 'Theoretical NEBP',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.nebp_response, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('responses_theoretical.png', dpi=300)
        plt.close(fig)

    def plot_responses(self):
        fig = plt.figure(51)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Response $s^{-1}$')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'green', 'marker': '^', 'markerfacecolor': 'None',
                 'markeredgecolor': 'green', 'linestyle': 'None', 'label': 'Theoretical Typical',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.typical_response, **style)
        style = {'color': 'blue', 'marker': 'o', 'markerfacecolor': 'None',
                 'markeredgecolor': 'blue', 'linestyle': 'None', 'label': 'Theoretical NEBP',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.nebp_response, **style)
        style = {'color': 'red', 'marker': 'x', 'markerfacecolor': 'None',
                 'markeredgecolor': 'red', 'linestyle': 'None', 'label': 'Experimental NEBP',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.experimental_responses, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('responses_comparison.png', dpi=300)
        plt.close(fig)

    def plot_diffs(self):
        diffs = abs(100 * (self.experimental_responses - self.nebp_response) / self.experimental_responses)
        fig = plt.figure(52)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Relative Error %')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'indigo', 'marker': 'd', 'markerfacecolor': 'None',
                 'markeredgecolor': 'indigo', 'linestyle': 'None', 'label': 'Theoretical NEBP',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, diffs, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('responses_error.png', dpi=250)
        plt.close(fig)

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
    do = Folding_Experiment()
