import matplotlib.pyplot as plt
import numpy as np
from nice_plots import Nice_Plots
from spectrum import Spectrum


class Plotter(object):
    def __init__(self):
        Nice_Plots()
        self.get_data()
        self.get_decker()
        self.set_coefficient()
        self.plot()
        self.plot_comparison()
        self.calc_peak_channels()

    def get_data(self):
        self.data = np.loadtxt('nebp_response_functions.txt').reshape(7, -1, 4)

    def get_decker(self):
        self.decker_data = np.loadtxt('decker_data.txt').reshape(7, -1, 4)

    def set_coefficient(self):
        self.c = 1.774E-2 * (1/4)

    def set_colors(self, i):
        colors = ['k', 'r', 'b', 'm', 'g', 'navy', 'purple']
        return colors[i]

    def set_labels(self, i):
        labels = ['bare', '2"', '3"', '5"', '8"', '10"', '12"']
        return labels[i]

    def plot(self):
        plt.figure(68)
        for i, sphere in enumerate(self.data):
            sphere = sphere.T
            edges = np.insert(sphere[1], 0, 1E-11)
            vals = sphere[2] * self.c
            err = sphere[3] * vals
            s = Spectrum(edges, vals, err)
            c = self.set_colors(i)
            l = self.set_labels(i)
            plt.plot(s.stepu_x, s.stepu_y, color=c, label=l)
            plt.errorbar(s.midpoints, s.values, s.error, linestyle='None', capsize=0, color=c)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(1E-8, 20)
        plt.xlabel('energy $MeV$')
        plt.ylabel('response $cm^{2}$')
        plt.legend(loc=3)
        plt.savefig('nebp_response_functions.png', dpi=250)
        plt.close()

    def plot_comparison(self):
        for i, sphere in enumerate(self.data):
            plt.figure(60 + i)
            sphere = sphere.T
            edges = np.insert(sphere[1], 0, 1E-11)
            vals = sphere[2] * self.c
            err = sphere[3] * vals
            s = Spectrum(edges, vals, err)
            c = self.set_colors(i)
            l = self.set_labels(i)
            plt.plot(s.stepu_x, s.stepu_y, color=c, label=l + ' Boyington')
            plt.errorbar(s.midpoints, s.values, s.error, linestyle='None', capsize=0, color=c)
            sphere = self.decker_data[i].T
            edges = np.insert(sphere[1], 0, 1E-11)
            vals = sphere[2]
            err = sphere[3] * vals
            s = Spectrum(edges, vals, err)
            c = self.set_colors(i)
            l = self.set_labels(i)
            plt.plot(s.edges[1:], s.values, linestyle='--', color=c, label=l + ' Decker')
            plt.errorbar(s.edges[1:], s.values, s.error, linestyle='None', capsize=0, color=c)
            plt.xscale('log')
            plt.yscale('log')
            plt.xlim(1E-8, 20)
            plt.xlabel('energy $MeV$')
            plt.ylabel('response $cm^{2}$')
            plt.legend(loc=3)
            plt.savefig('rf_comp{}.png'.format(l), dpi=250)
            plt.close()

    def calc_peak_channels(self):
        peak_channels = []
        prev = []
        for i, sphere in enumerate(self.data):
            best = np.array([0, 1E-11, 0, 0])
            best_prev = np.array([0, 1E-11, 0, 0])
            for j, erg in enumerate(sphere):
                if erg[2] > best[2]:
                    best = erg
                    best_prev = sphere[j-1][1]
            peak_channels.append(best[1])
            prev.append(best_prev)
        print(peak_channels)
        print(prev)
        with open('peak_channels.txt', 'w+') as F:
            for i, ch in enumerate(peak_channels):
                F.write('{:10.6e} {:10.6e}\n'.format(prev[i], ch))
                     
            


if __name__ == '__main__':
    plot = Plotter()
