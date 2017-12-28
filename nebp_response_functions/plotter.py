import matplotlib.pyplot as plt
import numpy as np
from spectrum import Spectrum
from matplotlib import rc, rcParams


class Plotter(object):
    def __init__(self):
        self.nice_plots()
        self.get_data()
        self.get_decker()
        self.set_coefficient()
        self.plot()
        # self.plot_comparison()
        self.calc_peak_channels()

    def nice_plots(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 15
        rcParams.update({'figure.autolayout': True})

    def get_data(self):
        self.data = np.loadtxt('nebp_response_functions.txt').reshape(7, -1, 4)

    def get_decker(self):
        self.decker_data = np.loadtxt('decker_data.txt').reshape(7, -1, 4)

    def set_coefficient(self):
        self.c = 1.774E-2 * (1/4)

    def set_colors(self, i):
        colors = ['k', 'purple', 'blue', 'green', 'orange', 'red', 'brown']
        return colors[i]

    def set_linestyles(self, i):
        lines = ['-', '-.', '--', ':', '-', '-.', '--']
        return lines[i]

    def set_labels(self, i):
        labels = ['Bare', '2"', '3"', '5"', '8"', '10"', '12"']
        return labels[i]

    def plot(self):
        fig = plt.figure(68)
        ax = fig.add_subplot(111)
        for i, sphere in enumerate(self.data):
            sphere = sphere.T
            edges = np.insert(sphere[1], 0, 1E-11)
            vals = sphere[2] * self.c
            err = sphere[3] * vals
            s = Spectrum(edges, vals, err)
            style = {'color': self.set_colors(i), 'linestyle': self.set_linestyles(i),
                     'linewidth': 0.7, 'label': self.set_labels(i)}
            ax.plot(s.stepu_x, s.stepu_y, **style)
            style = {'color': self.set_colors(i), 'linestyle': 'None', 'linewidth': 0.7}
            ax.errorbar(s.midpoints, s.values, s.error, **style)
            if i == 0:
                plus = 5E-3
            else:
                plus = 0
            ax.text(1.2E-8, s.stepu_y[1] + plus, self.set_labels(i))
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(1E-8, 20)
        ax.set_xlabel('Energy $MeV$')
        ax.set_ylabel('Response $cm^{2}$')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.savefig('nebp_response_functions.png', dpi=300)
        plt.close(fig)

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
