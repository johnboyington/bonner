import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from spectrum import Spectrum  # located in my python_modules repo: https://github.com/johnboyington/python_modules
from nebp_spectrum import FluxNEBP  # located in my python_modules repo: https://github.com/johnboyington/python_modules
from folding import Folding
import experimental_data


class Folding_Experiment(object):

    def __init__(self):
        self.nice_plots()
        self.set_coefficient()
        self.sizes = [0, 2, 3, 5, 8, 10, 12]
        self.fold_nebp()
        self.fold_filtered()
        self.plot_responses()
        self.plot_filtered()
        self.plot_diffs()

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
        # TODO: find out what the hell this is
        self.c = 1.774E-2 * (1/4)

    def fold_filtered(self):
        # input response matrix
        genericData = np.loadtxt('nebp_response_functions.txt')
        genericData = genericData.reshape(7, -1, 4)
        rfs = genericData[:, :, 2]

        # produce spectrum object for nebp
        bins = np.loadtxt('scale56.txt')
        # calculate neutron scaling factor
        tally_area = tally_area = np.pi * (1.27 ** 2)
        cn = 2.54 / (200 * 1.60218e-13 * tally_area)
        cn *= 7.53942E-8
        cn *= 250  # normalize to 250 W(th)
        n_fil = np.loadtxt('n_fil2.txt')
        n_fil = n_fil.T[1][1:] * cn
        f = Spectrum(bins, n_fil)

        # create and test object
        fold = Folding(sf=self.c)
        fold.set_spectrum(f)
        print('Typical total flux: {}'.format(fold.spectrum.total_flux))
        fold.set_response_functions(rfs)
        self.filtered_response = fold.fold()

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

    def plot_responses(self):
        fig = plt.figure(51)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Response $s^{-1}$')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'red', 'marker': 'x', 'markerfacecolor': 'None',
                 'markeredgecolor': 'red', 'linestyle': 'None', 'label': 'Theoretical',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.nebp_response, **style)
        style = {'color': 'blue', 'marker': 'o', 'markerfacecolor': 'None',
                 'markeredgecolor': 'blue', 'linestyle': 'None', 'label': 'Experiment #1',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, experimental_data.unfiltered1.values, **style)
        style = {'color': 'green', 'marker': '^', 'markerfacecolor': 'None',
                 'markeredgecolor': 'green', 'linestyle': 'None', 'label': 'Experiment #2',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, experimental_data.unfiltered2.values, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('responses_comparison.png', dpi=300)
        plt.close(fig)

    def plot_filtered(self):
        fig = plt.figure(51)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Response $s^{-1}$')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'darkorange', 'marker': 'p', 'markerfacecolor': 'None',
                 'markeredgecolor': 'darkorange', 'linestyle': 'None', 'label': 'Theoretical NEBP Filtered',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.filtered_response, **style)
        style = {'color': 'indigo', 'marker': 'd', 'markerfacecolor': 'None',
                 'markeredgecolor': 'indigo', 'linestyle': 'None', 'label': 'Experiment #1 NEBP Filtered',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, experimental_data.filtered2.values, **style)
        style = {'color': 'darkgreen', 'marker': 'v', 'markerfacecolor': 'None',
                 'markeredgecolor': 'darkgreen', 'linestyle': 'None', 'label': 'Experiment #2 NEBP Filtered',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, experimental_data.filtered3.values, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.set_yscale('log')
        ax.legend()
        fig.savefig('responses_filtered.png', dpi=300)
        plt.close(fig)

    def plot_diffs(self):
        diffs1 = 100 * ((experimental_data.unfiltered1.values - self.nebp_response) / experimental_data.unfiltered1.values)
        diffs2 = 100 * ((experimental_data.unfiltered2.values - self.nebp_response) / experimental_data.unfiltered2.values)
        fig = plt.figure(52)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Relative Error %')
        ax.set_xlabel('Sphere Size $in$')
        style = {'color': 'blue', 'marker': 'o', 'markerfacecolor': 'None',
                 'markeredgecolor': 'blue', 'linestyle': 'None', 'label': 'Experiment #1',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, diffs1, **style)
        style = {'color': 'green', 'marker': '^', 'markerfacecolor': 'None',
                 'markeredgecolor': 'green', 'linestyle': 'None', 'label': 'Experiment #2',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, diffs2, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('responses_error.png', dpi=250)
        plt.close(fig)


if __name__ == '__main__':
    Folding_Experiment()
