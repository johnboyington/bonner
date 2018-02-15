import values
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


class Plot(object):
    def __init__(self):
        self.err_tol = 0.2
        self.energies = values.energies
        self.make_image(0)

    def load_data(self, flag):
        self.data = np.loadtxt('data.txt')
        self.data = self.data.T
        self.data = self.data[flag]
        self.max = max(self.data)
        self.min = min(self.data)
        self.data = self.data.reshape(values.numy, values.numz, len(self.energies))
        self.totals = self.data[:, :, -1]
        self.data = self.data[:, :, :-1]

    def make_image(self, flag):
        self.load_data(flag)
        fig = plt.figure(999, figsize=(9.62, 5.08))
        ax = fig.add_subplot(111)
        ax.set_xlabel('y')
        ax.set_ylabel('z')
        ax.set_title('Total $\Phi$')
        if flag:
            for i, a in enumerate(self.totals):
                for j, b in enumerate(a):
                    if self.totals[i, j] == 0:
                        self.totals[i, j] = 1
                    if self.totals[i, j] < self.err_tol:
                        self.totals[i, j] = 0.0
        args = {'aspect': 'auto', 'cmap': 'pink', 'extent': [-7.62, 7.62, -5.08, 5.08], 'vmin': self.min, 'vmax': self.max}
        im = ax.imshow(self.totals, **args)
        circ = Circle((0, 0), 2.54/2, fill=False)
        ax.add_patch(circ)
        fig.colorbar(im)
'''
        for i, e in enumerate(self.energies[-1::-1]):
            group = len(self.energies[:-2]) - i
            fig = plt.figure(i, figsize=(9.62, 5.08))
            ax = fig.add_subplot(111)
            ax.set_xlabel('y')
            ax.set_ylabel('z')
            ax.set_title('Group {}'.format(i))
            args = {'aspect': 'auto', 'cmap': 'pink', 'extent': [-7.62, 7.62, -5.08, 5.08], 'vmin': self.min, 'vmax': self.max}
            im = ax.imshow(self.data[:, :, group], **args)
            circ = Circle((0, 0), 2.54/2, fill=False)
            ax.add_patch(circ)
            fig.colorbar(im)
'''


Plot()
