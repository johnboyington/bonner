import numpy as np
import matplotlib.pyplot as plt


class FluxNEBP():
    """
    This class contains information on the nebp obtained from an mcnp analysis
    of the ksu triga mark II north east beam port.
    
    Input reactor power in W(th)
    """

    def __init__(self, P):
        self.power = P
        self.data = self.store_data()
        self.num_bins, self.num_edges = self.count_bins()
        self.edges = self.data[:, 0]
        self.values = self.normalize_values()
        self.error = self.data[:, 2]
        self.widths = self.edges[1:] - self.edges[:-1]
        self.normalized_values = self.values[1:] / self.widths
        self.step_x, self.step_y = self.make_step()
    
    
    
    
    
    
    
    
    
    def store_data(self):
        data = np.loadtxt('nebp_data.txt')
        return data

    def count_bins(self):
        l = len(self.data)
        return l - 1, l

    def normalize_values(self):
        tally_area = tally_area = np.pi * (1.27 ** 2)
        C = 2.54 / (200 * 1.60218e-13 * tally_area)
        return self.data[:, 1] * C * self.power

    def make_step(self):
        assert len(self.edges) - 1 == len(self.normalized_values), 'x - 1 != y'
        Y = np.array([[yy, yy] for yy in np.array(self.normalized_values)]).flatten()
        X = np.array([[xx, xx] for xx in np.array(self.edges)]).flatten()[1:-1]
        return X, Y

    def plot(self):
        plt.figure(99)
        plt.plot(self.step_x, self.step_y)
        plt.xlabel('Energy MeV')
        plt.ylabel('Flux $MeV^{-1}cm^{-2}s^{-1}$')
        plt.xlim(1E-8, 20)
        plt.xscale('log')
        plt.yscale('log')


if True:
    flux = FluxNEBP(250)
