import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from spectrum import Spectrum  # located in my python_modules repo: https://github.com/johnboyington/python_modules
from lwr_spectrum import FluxTypical  # located in my python_modules repo: https://github.com/johnboyington/python_modules
from nebp_spectrum import FluxNEBP  # located in my python_modules repo: https://github.com/johnboyington/python_modules


class Plot(object):

    def __init__(self):
        self.load_data()
        print('Producing Plots...')
        self.nice_plots()
        self.plot_all()
        print('   Finished Plotting')

    def load_dataset(self, name):
        data = np.loadtxt('data/{}_unfolded.txt'.format(name))
        data = data.T
        self.data['{}'.format(name)] = Spectrum(self.edges, data[1], data[2], dfde=True)

    def load_data(self):
        # load scale56 bin edges
        self.edges = np.loadtxt('scale56.txt')

        # load typical lwr spectrum
        sf = 294858.046942 / 0.0263292381867
        self.typical_spectrum = FluxTypical(self.edges, sf, 1./7., 600.0)
        self.typical_spectrum.change_bins(self.edges)

        # load nebp spectrum
        self.nebp_spectrum = FluxNEBP(250)

        # load filtered spectrum
        # calculate neutron scaling factor
        tally_area = tally_area = np.pi * (1.27 ** 2)
        cn = 2.54 / (200 * 1.60218e-13 * tally_area)
        cn *= 7.53942E-8
        cn *= 250  # normalize to 250 W(th)
        n_fil = np.loadtxt('n_fil2.txt')
        n_fil = n_fil.T[1][1:] * cn
        self.filtered_spectrum = Spectrum(self.edges, n_fil)

        # load unity spectrum
        ones = np.ones(len(self.edges) - 1)
        self.unity_spectrum = Spectrum(self.edges, ones, dfde=True)

        # load unfolded data
        self.data = {}
        self.datasets = ['e1_ne_gr', 'e1_ne_mx',
                         'e2_ne_gr', 'e2_ne_mx',
                         'f2_ne_gr', 'f2_ne_mx',
                         'f2_fi_gr', 'f2_fi_mx',
                         'f2_un_gr', 'f2_un_mx',
                         'f3_ne_gr', 'f3_ne_mx',
                         'f3_fi_gr', 'f3_fi_mx',
                         'f3_un_gr', 'f3_un_mx']
        for name in self.datasets:
            self.load_dataset(name)

    def nice_plots(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 15
        rcParams.update({'figure.autolayout': True})

    def plot_all(self):
        self.plot('e1_ne_gr', 'e1_ne_mx', '1', self.nebp_spectrum, (1E2, 1E13))
        self.plot('e2_ne_gr', 'e2_ne_mx', '2', self.nebp_spectrum, (1E2, 1E13))

        # first set of filtered results
        self.plot('f2_ne_gr', 'f2_ne_mx', 'fil2', self.nebp_spectrum, (1E2, 1E13))
        self.plot('f2_un_gr', 'f2_un_mx', 'fil2_unity', self.unity_spectrum, (1E-1, 1E11))
        self.plot('f2_fi_gr', 'f2_fi_mx', 'fil2_filtered', self.filtered_spectrum, (1E0, 1E13))

        # second set of filtered results
        self.plot('f3_ne_gr', 'f3_ne_mx', 'fil3', self.nebp_spectrum, (1E2, 1E13))
        self.plot('f3_un_gr', 'f3_un_mx', 'fil3_unity', self.unity_spectrum, (1E-1, 1E11))
        self.plot('f3_fi_gr', 'f3_fi_mx', 'fil3_filtered', self.filtered_spectrum, (1E0, 1E13))

    def plot(self, name1, name2, savename, ds, ylims=False):
        fig = plt.figure(0)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(*ylims)

        style = {'color': 'red',  'linewidth': 0.7, 'label': 'Default Spectrum'}
        ax.plot(ds.step_x, ds.step_y, **style)
        style = {'color': 'green', 'linestyle': '--', 'linewidth': 0.7, 'label': 'Gravel'}
        ax.plot(self.data[name1].step_x, self.data[name1].step_y, **style)
        style = {'color': 'blue', 'linestyle': '-.', 'linewidth': 0.7, 'label': 'Maxed'}
        ax.plot(self.data[name2].step_x, self.data[name2].step_y, **style)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('plots/unfolded_{}.png'.format(savename), dpi=300)
        plt.close(fig)

        # groupwise ratios
        fig = plt.figure(3)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Ratio $\phi / \phi_{default}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(1E-2, 1E2)

        style = {'color': 'black',  'linewidth': 0.7, 'label': 'Reference'}
        ax.plot([1E-11, 20], [1, 1], **style)

        gravel_ratio = abs(self.data[name1].step_y / ds.step_y)
        style = {'color': 'green',  'linewidth': 0.7, 'label': 'Gravel'}
        ax.plot(self.data[name1].step_x, gravel_ratio, **style)

        maxed_ratio = abs(self.data[name2].step_y / ds.step_y)
        style = {'color': 'blue',  'linewidth': 0.7, 'label': 'Maxed'}
        ax.plot(self.data[name2].step_x, maxed_ratio, **style)

        ax.fill_between(ds.step_x, 1, maxed_ratio, facecolor='blue', alpha=0.2)
        ax.fill_between(ds.step_x, 1, gravel_ratio, facecolor='green', alpha=0.2)

        ax.legend(frameon=False)
        fig.savefig('plots/unfolded_{}_ratios.png'.format(savename), dpi=300)
        plt.close(fig)

if __name__ == '__main__':
    Plot()
