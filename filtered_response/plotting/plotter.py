import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
import numpy as np


class Plot(object):
    def __init__(self):
        self.nice_plots()
        self.sizes = [0, 2, 3, 5, 8, 10, 12]
        self.grab_data()
        self.plot_responses()

    def nice_plots(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 15
        rcParams.update({'figure.autolayout': True})

    def grab_data(self):
        # load and normalize mcnp data
        self.mcnp = np.loadtxt('filtered_responses_mcnp.txt')
        self.mcnp = self.mcnp[:, 1]
        filtered_flux_sf = 0.022084400339 * 294858.0469
        self.mcnp *= filtered_flux_sf * 3E-3  # just guessing a scaling factor

        # load normalized experimental data
        self.experimental = np.loadtxt('e2f.nr')

    def plot_responses(self):
        fig = plt.figure(50)
        ax = fig.add_subplot(111)
        ax.set_ylabel('Response $s^{-1}$')
        ax.set_xlabel('Sphere Size $in$')

        # plot experimental results
        style = {'color': 'blue', 'marker': 'o', 'markerfacecolor': 'None',
                 'markeredgecolor': 'blue', 'linestyle': 'None', 'label': 'Experimental',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.experimental[0], **style)
        # errorbar
        style = {'color': 'blue', 'elinewidth': 0.5, 'fmt': None}
        ax.errorbar(self.sizes, self.experimental[0], self.experimental[1], **style)

        # plot mcnp results
        style = {'color': 'green', 'marker': '^', 'markerfacecolor': 'None',
                 'markeredgecolor': 'green', 'linestyle': 'None', 'label': 'MCNP',
                 'mew': 0.5, 'ms': 6}
        ax.plot(self.sizes, self.mcnp, **style)
        ax.set_xticks(self.sizes)
        ax.set_xticklabels(['Bare'] + self.sizes[1:])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()
        fig.savefig('filtered_responses.png', dpi=300)
        plt.close(fig)

Plot()
