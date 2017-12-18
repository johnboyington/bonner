import numpy as np
import matplotlib.pyplot as plt
from spectrum import Spectrum
from lwr_spectrum import FluxTypical
from nebp_spectrum import FluxNEBP


class Plot(object):

    def __init__(self):
        self.load_data()
        self.plot_experimental_nebp()

    def load_data(self):
        # load scale56 bin edges
        self.edges = np.loadtxt('scale56.txt')

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

    def plot_experimental_nebp(self):
        plt.figure(0)
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(self.nebp_spectrum.step_x, self.nebp_spectrum.step_y, 'k', label='default spectrum')
        plt.plot(self.data['ex_ne_gr'].step_x, self.data['ex_ne_gr'].step_y, 'r', label='gravel')
        plt.plot(self.data['ex_ne_mx'].step_x, self.data['ex_ne_mx'].step_y, 'r--', label='maxed')
        plt.legend()
        plt.savefig('unfolded.png', dpi=300)
        plt.close()


Plot()
