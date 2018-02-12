import matplotlib.pyplot as plt
import numpy as np


class Plot(object):
    def __init__(self):
        self.load_data()
        self.make_image()

    def load_data(self):
        self.data = np.loadtxt('data.txt')
        self.data = self.data.T
        self.data = self.data[0]
        self.data = self.data.reshape(9, 9)

    def make_image(self):
        fig = plt.figure(0, figsize=(9.62, 5.08))
        ax = fig.add_subplot(111)
        im = ax.imshow(self.data, aspect='auto', cmap='YlGnBu')
        fig.colorbar(im)
        ax.set_xlabel('y')
        ax.set_ylabel('z')

Plot()
