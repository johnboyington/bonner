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
        self.plot_experimental_nebp()
        self.plot_theoretical_nebp()
        print('   Finished Plotting')

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

        # load unfolded data
        self.data = {}
        data = np.loadtxt('data/ex_ne_gr_unfolded.txt')
        data = data.T
        self.data['ex_ne_gr'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/ex_ne_mx_unfolded.txt')
        data = data.T
        self.data['ex_ne_mx'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/ex_ty_gr_unfolded.txt')
        data = data.T
        self.data['ex_ty_gr'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/ex_ty_mx_unfolded.txt')
        data = data.T
        self.data['ex_ty_mx'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/th_ne_gr_unfolded.txt')
        data = data.T
        self.data['th_ne_gr'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/th_ne_mx_unfolded.txt')
        data = data.T
        self.data['th_ne_mx'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/th_ty_gr_unfolded.txt')
        data = data.T
        self.data['th_ty_gr'] = Spectrum(self.edges, data[1], data[2], dfde=True)

        data = np.loadtxt('data/th_ty_mx_unfolded.txt')
        data = data.T
        self.data['th_ty_mx'] = Spectrum(self.edges, data[1], data[2], dfde=True)

    def nice_plots(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 15
        rcParams.update({'figure.autolayout': True})

    def plot_experimental_nebp(self):
        fig = plt.figure(0)
        ax = fig.add_subplot(111)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        ax.set_xlim(1E-9, 20)
        ax.set_ylim(1E2, 1E13)

        style = {'color': 'red',  'linewidth': 0.7, 'label': 'default spectrum'}
        ax.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, **style)
        style = {'color': 'green', 'linestyle': '--', 'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data['ex_ne_gr'].step_x, self.data['ex_ne_gr'].step_y, **style)
        style = {'color': 'blue', 'linestyle': '-.', 'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data['ex_ne_mx'].step_x, self.data['ex_ne_mx'].step_y, **style)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded.png', dpi=300)
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
        ax.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, **style)
        style = {'color': 'blue', 'linestyle': '-.', 'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data['ex_ne_mx'].step_x, self.data['ex_ne_mx'].step_y, **style)

        ax.fill_between(self.nebp_spectrum.step_x, 0, self.nebp_spectrum.step_y, facecolor='red', alpha=0.2)
        ax.fill_between(self.nebp_spectrum.step_x, 0, self.data['ex_ne_mx'].step_y, facecolor='blue', alpha=0.2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded_maxed_only.png', dpi=300)
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
        ax.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, **style)
        style = {'color': 'green', 'linestyle': '--', 'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data['ex_ne_gr'].step_x, self.data['ex_ne_gr'].step_y, **style)

        ax.fill_between(self.nebp_spectrum.step_x, 0, self.nebp_spectrum.step_y, facecolor='red', alpha=0.2)
        ax.fill_between(self.nebp_spectrum.step_x, 0, self.data['ex_ne_gr'].step_y, facecolor='green', alpha=0.2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False)
        fig.savefig('unfolded_gravel_only.png', dpi=300)
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

        gravel_ratio = abs(self.data['ex_ne_gr'].step_y / self.nebp_spectrum.step_y)
        style = {'color': 'green',  'linewidth': 0.7, 'label': 'gravel'}
        ax.plot(self.data['ex_ne_gr'].step_x, gravel_ratio, **style)

        maxed_ratio = abs(self.data['ex_ne_mx'].step_y / self.nebp_spectrum.step_y)
        style = {'color': 'blue',  'linewidth': 0.7, 'label': 'maxed'}
        ax.plot(self.data['ex_ne_mx'].step_x, maxed_ratio, **style)
        for i, bounds in enumerate(self.peak_channels):
            l, r = bounds
            if i == 0:
                lab = 'peak channels'
            else:
                lab = None
            style = {'color': 'gold', 'marker': '|',  'linewidth': 0.7, 'label': lab}
            ax.plot([l, r], [1, 1], **style)

        ax.fill_between(self.nebp_spectrum.step_x, 1, maxed_ratio, facecolor='blue', alpha=0.2)
        ax.fill_between(self.nebp_spectrum.step_x, 1, gravel_ratio, facecolor='green', alpha=0.2)

        ax.legend(frameon=False)
        fig.savefig('unfolded_ratios.png', dpi=300)
        plt.close(fig)

    def plot_theoretical_nebp(self):
        plt.figure(0)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Energy $MeV$')
        plt.ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        plt.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, 'k', label='default spectrum')
        plt.plot(self.data['th_ne_gr'].step_x, self.data['th_ne_gr'].step_y, 'r', label='gravel')
        plt.plot(self.data['th_ne_mx'].step_x, self.data['th_ne_mx'].step_y, 'b', label='maxed')
        plt.legend()
        plt.savefig('unfolded_theoretical.png', dpi=300)
        plt.close()

        # only maxed
        plt.figure(1)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Energy $MeV$')
        plt.ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        plt.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, 'k', label='default spectrum')
        plt.plot(self.data['th_ne_mx'].step_x, self.data['th_ne_mx'].step_y, 'b', label='maxed')
        plt.legend()
        plt.savefig('unfolded_theoretical_maxed_only.png', dpi=300)
        plt.close()

        # only gravel
        plt.figure(2)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Energy $MeV$')
        plt.ylabel('Flux $cm^{-2}s^{-1}MeV^{-1}$')
        plt.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, 'k', label='default spectrum')
        plt.plot(self.data['th_ne_gr'].step_x, self.data['th_ne_gr'].step_y, 'r', label='gravel')
        plt.legend()
        plt.savefig('unfolded_theoretical_gravel_only.png', dpi=300)
        plt.close()

        # groupwise ratios
        plt.figure(3)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Energy $MeV$')
        plt.ylabel('Ratio $\phi / \phi_{default}$')
        plt.plot([1E-11, 20], [1, 1], 'k', label='reference')
        gravel_ratio = abs(self.data['th_ne_gr'].step_y / self.nebp_spectrum.step_y)
        plt.plot(self.data['th_ne_gr'].step_x, gravel_ratio, 'r', label='gravel')
        maxed_ratio = abs(self.data['th_ne_mx'].step_y / self.nebp_spectrum.step_y)
        plt.plot(self.data['th_ne_mx'].step_x, maxed_ratio, 'b', label='maxed')
        for i, bounds in enumerate(self.peak_channels):
            l, r = bounds
            if i == 0:
                lab = 'peak channels'
            else:
                lab = None
            plt.plot([l, r], [1, 1], 'gold', marker='|', label=lab)
        plt.legend()
        plt.savefig('unfolded_theoretical_ratios.png', dpi=300)
        plt.close()


Plot()
