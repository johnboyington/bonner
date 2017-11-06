import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


class Spectrum(object):

    def __init__(self, data, S=1, dfde=False):
        assert data.shape[1] == 2 or data.shape[1] == 3, 'Spectral data {} does not match input format'.format(data.shape)
        self.scaling_factor = S
        self.data = data
        self.num_bins, self.num_edges = self.count_bins()
        self.edges = self.data[:, 0]
        self.values = self.scale_values()
        self.total_flux = np.sum(self.values)
        if self.data.shape[1] == 3:
            self.error = self.data[:, 2]
        else:
            self.error = self.estimate_error()
        self.widths = self.edges[1:] - self.edges[:-1]
        if dfde:
            self.normalized_values = self.values[1:]
            self.values = self.values[1:] * self.widths
        else:
            self.normalized_values = self.values[1:] / self.widths
        self.step_x, self.step_y = self.make_step()

    def count_bins(self):
        '''Counts the number of bins and bin edges in the data'''
        l = len(self.data)
        return l - 1, l

    def scale_values(self):
        '''Normalizes values to given scaling factor'''
        return self.data[:, 1] * self.scaling_factor

    def estimate_error(self):
        '''If error is not given, '''
        return np.full(len(self.values), 0.05)

    def make_step(self):
        '''Make the binned flux data able to be plotted with plt.plot'''
        assert len(self.edges) - 1 == len(self.normalized_values), 'x - 1 != y'
        Y = np.array([[yy, yy] for yy in np.array(self.normalized_values)]).flatten()
        X = np.array([[xx, xx] for xx in np.array(self.edges)]).flatten()[1:-1]
        return X, Y

    def functional_form(self, E):
        '''Produce a function from the step data (for use in integration)'''
        val = 0
        for i, v in enumerate(self.normalized_values):
            if E >= self.edges[i] and E < self.edges[i+1]:
                val = v
        return val

    def change_bins(self, bins):
        '''Makes discrete energy groups from continuous function above, given a desired bin structure.
        TODO: Change method of integration.'''
        bin_values = [0.00]
        for i in range(len(bins) - 1):
            area, err = quad(self.functional_form, bins[i], bins[i+1])
            height = area / (bins[i+1] - bins[i])
            bin_values.append(height)
        new_data = np.array([bins, bin_values]).T
        Spectrum.__init__(self, new_data)
        return bin_values

    def plot(self):
        '''Plot flux data'''
        plt.figure(99)
        plt.plot(self.step_x, self.step_y)
        plt.xlabel('Energy MeV')
        plt.ylabel('Flux $MeV^{-1}cm^{-2}s^{-1}$')
        plt.xlim(1E-8, 20)
        plt.xscale('log')
        plt.yscale('log')
