import matplotlib.pyplot as plt
import numpy as np
from nice_plots import Nice_Plots
from spectrum import Spectrum


class Plotter(object):
    def __init__(self, good=False):
        init_nice_plotting = Nice_Plots()
        self.get_data()
        self.set_coefficient()
        if good:
            self.plot()
        else:
            self.plot_no_working()
        
    
    def get_data(self):
        self.data = np.loadtxt('nebp_response_functions.txt').reshape(7, -1, 4)
    
    def set_coefficient(self):
        pass
    
    def plot_no_working(self):
        plt.figure(0)
        for sphere in self.data:
            sphere = sphere.T
            edges = np.insert(sphere[1], 0, 1E-11)
            vals = np.insert(sphere[2], 0, 0)
            
            s = Spectrum(edges, vals)
            plt.plot(s.stepu_x, s.stepu_y)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(1E-9, 20)
    
    def plot(self):
        plt.figure(0)
        for sphere in self.data:
            sphere = sphere.T
            
            plt.plot(sphere[1], sphere[2])
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(1E-9, 20)


if __name__ == '__main__':
    plot = Plotter(good=False)