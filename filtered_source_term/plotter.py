import values
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D


class Plot(object):
    def __init__(self):
        '''Function that is called when the class is initialized.'''
        flag = 0
        self.err_tol = 0.2
        self.energies = values.energies
        self.load_data(flag)
        self.make_image(flag)
        self.make_3d()

    def load_data(self, flag):
        # load in data from file
        self.data = np.loadtxt('data/data.txt', skiprows=3)
        # transpose data matrix
        self.data = self.data.T
        # grab either the values or the errors (flag 0 or 1)
        self.data = self.data[flag]
        # grab the max and min of the data
        self.max = max(self.data)
        self.min = min(self.data)
        # reshape into a 3d array
        self.data = self.data.reshape(values.numy, values.numz, len(self.energies))
        # grab the totals from the array
        self.totals = self.data[:, :, -1]
        # remove the totals from the data
        self.data = self.data[:, :, :-1]

    def make_image(self, flag):
        # open up the plotting figure
        fig = plt.figure(999, figsize=(9.62, 5.08))
        # add axes to the plot
        ax = fig.add_subplot(111)
        # set the labels and title on the plot
        ax.set_xlabel('y')
        ax.set_ylabel('z')
        ax.set_title('Total $\Phi$')
        # if plotting error, makes all errors below the tolerance 0
        # and sets all unscored bins (therefore no error) to 100% error
        if flag:
            for i, a in enumerate(self.totals):
                for j, b in enumerate(a):
                    if self.totals[i, j] == 0:
                        self.totals[i, j] = 1
                    if self.totals[i, j] < self.err_tol:
                        self.totals[i, j] = 0.0
        # the series of arguments for the plot
        args = {'aspect': 'auto', 'cmap': 'pink', 'extent': [-7.62, 7.62, -5.08, 5.08], 'vmin': self.min, 'vmax': self.max}
        im = ax.imshow(self.totals.T, **args)
        # contour plot instead of image
        # im = ax.contourf(self.totals, **args)
        # add a circle to the plot to show beam port size
        circ = Circle((0, 0), 2.54/2, fill=False)
        ax.add_patch(circ)
        # add a colorbar to the image
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
            im = ax.imshow(self.data[:, :, group].T, **args)
            circ = Circle((0, 0), 2.54/2, fill=False)
            ax.add_patch(circ)
            fig.colorbar(im)
        '''

    def make_3d(self):
        # calculate the midpoints of each pixel
        self.y_div = np.linspace(values.y_min, values.y_max, values.numy + 1)
        self.y_mids = (self.y_div[1:] + self.y_div[:-1]) / 2
        # repeat for z values
        self.z_div = np.linspace(values.z_min, values.z_max, values.numz + 1)
        self.z_mids = (self.z_div[1:] + self.z_div[:-1]) / 2

        # create x and y points for 3d plotting
        xx, yy = np.meshgrid(self.y_mids, self.z_mids)
        fig = plt.figure(0)
        ax = fig.add_subplot(111, projection='3d')
        # make surface plot
        ax.plot_surface(xx, yy, self.totals.T, cmap='plasma')
        ax.set_xlabel('y')
        ax.set_ylabel('z')
        plt.show()


Plot()
