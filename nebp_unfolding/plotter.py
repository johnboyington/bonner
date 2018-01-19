import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from spectrum import Spectrum
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP


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

        # load peak channels
        self.peak_channels = np.loadtxt('peak_channels.txt')

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

        # load unfolded data
        self.data = {}
        self.datasets = ['ex_ne_gr', 'ex_ne_mx',
                         'e2_ne_gr', 'e2_ne_mx',
                         'e3_ne_gr', 'e3_ne_mx',
                         'e3_fi_gr', 'e3_fi_mx',
                         'th_ne_gr', 'th_ne_mx']
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
        self.plot('ex_ne_gr', 'ex_ne_mx', '1', self.nebp_spectrum)
        self.plot('e2_ne_gr', 'e2_ne_mx', '2', self.nebp_spectrum)
        self.plot('e3_ne_gr', 'e3_ne_mx', '3', self.nebp_spectrum)
        self.plot('e3_fi_gr', 'e3_fi_mx', 'filtered', self.filtered_spectrum)
        self.plot('th_ne_gr', 'th_ne_mx', 'theoretical', self.nebp_spectrum)

    def plot(self, name1, name2, savename, ds):
        fig = plt.figure(0)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(1E2, 1E13)

        style = {'color': 'red',  'linewidth': 0.7, 'label': 'default spectrum'}
        ax.plot(ds.step_x, ds.step_y, **style)
        style = {'color': 'green', 'linestyle': '--', 'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data[name1].step_x, self.data[name1].step_y, **style)
        style = {'color': 'blue', 'linestyle': '-.', 'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data[name2].step_x, self.data[name2].step_y, **style)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded_{}.png'.format(savename), dpi=300)
        plt.close(fig)

        # only maxed
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(1E2, 1E13)

        style = {'color': 'red',  'linewidth': 0.7, 'label': 'default spectrum'}
        ax.plot(ds.step_x, ds.step_y, **style)
        style = {'color': 'blue', 'linestyle': '-.', 'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data[name2].step_x, self.data[name2].step_y, **style)

        ax.fill_between(ds.step_x, 0, ds.step_y, facecolor='red', alpha=0.2)
        ax.fill_between(ds.step_x, 0, self.data[name2].step_y, facecolor='blue', alpha=0.2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded_{}_maxed_only.png'.format(savename), dpi=300)
        plt.close(fig)

        # only gravel
        fig = plt.figure(2)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(1E2, 1E13)

        style = {'color': 'red',  'linewidth': 0.7, 'label': 'default spectrum'}
        ax.plot(ds.step_x, ds.step_y, **style)
        style = {'color': 'green', 'linestyle': '--', 'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data[name1].step_x, self.data[name1].step_y, **style)

        ax.fill_between(ds.step_x, 0, ds.step_y, facecolor='red', alpha=0.2)
        ax.fill_between(ds.step_x, 0, self.data[name1].step_y, facecolor='green', alpha=0.2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded_{}_gravel_only.png'.format(savename), dpi=300)
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

        style = {'color': 'black',  'linewidth': 0.7, 'label': 'reference'}
        ax.plot([1E-11, 20], [1, 1], **style)

        gravel_ratio = abs(self.data[name1].step_y / ds.step_y)
        style = {'color': 'green',  'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data[name1].step_x, gravel_ratio, **style)

        maxed_ratio = abs(self.data[name2].step_y / ds.step_y)
        style = {'color': 'blue',  'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data[name2].step_x, maxed_ratio, **style)

        ax.fill_between(ds.step_x, 1, maxed_ratio, facecolor='blue', alpha=0.2)
        ax.fill_between(ds.step_x, 1, gravel_ratio, facecolor='green', alpha=0.2)

        ax.legend(frameon=False)
        fig.savefig('unfolded_{}_ratios.png'.format(savename), dpi=300)
        plt.close(fig)

if __name__ == '__main__':
    Plot()
