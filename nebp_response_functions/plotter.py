import matplotlib.pyplot as plt
import numpy as np
from nice_plots import Nice_Plots
from spectrum import Spectrum


class Plotter(object):
    def __init__(self):
        Nice_Plots()
        self.get_data()
        self.set_coefficient()
        self.plot()

    def get_data(self):
        self.data = np.loadtxt('nebp_response_functions.txt').reshape(7, -1, 4)

    def set_coefficient(self):
        self.c = 1.774E-2 * (1/4)

    def set_colors(self, i):
        colors = ['blue', 'green', 'red', 'black', 'orange', 'violet', 'yellow']
        return colors[i]

    def set_labels(self, i):
        labels = ['bare', '2"', '3"', '5"', '8"', '10"', '12"']
        return labels[i]

    def plot(self):
        plt.figure(0)
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
        plt.xlim(1E-9, 20)
        plt.xlabel('energy $MeV$')
        plt.ylabel('response $cm^{-2}$')
        plt.legend(loc=3)
        plt.savefig('nebp_response_functions.png', dpi=250)


if __name__ == '__main__':
    plot = Plotter()
