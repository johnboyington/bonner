import values
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Source(object):
    def __init__(self):
        self.s = ''
        self.energies = values.energies
        self.load_data()
        self.cals_divs()
        self.write_header()
        self.add_positions()

    def load_data(self):
        ''' Loads the source data in from a text file and parses out the
        totals and the data while removing the error'''
        self.data = np.loadtxt('data.txt')
        self.data = self.data.T
        self.data = self.data[0]
        self.data = self.data.reshape(values.numy, values.numz, len(self.energies))
        self.totals = self.data[:, :, -1]
        self.data = self.data[:, :, :]  # keep last column as opposed to plotter

    def write_header(self):
        '''Writes the header for the MCNP SDEF'''
        self.s += 'c  ---------------------------------------------------------\n'
        self.s += 'c                    SOURCE SPECIFICATIONS\n'
        self.s += 'c                    For the Filtered NEBP\n'
        self.s += 'c  ---------------------------------------------------------\n'
        self.s += 'SDEF    X=0 Y=D1 Z=D2 POS=D3  ERG=FPOS=D4 \n'
        self.s += '        DIR=1 PAR=1 AXS=1 0 0 VEC=1 0 0\n'

    def card(self, card, data, elements=5):
        '''
        Function: cardWriter

        This will write multiline cards for SI and SP distributions for mcnp inputs

        Input Data:
            card - name and number of the card
            data array - a numpy array containing the data you'd like placed in the card.
            Outputs:
                a string that can be copied and pasted into an mcnp input file
        '''
        s = '{}   '.format(card)
        empty_card = '   ' + ' ' * len(card)
        elements_per_row = elements
        row_counter = 0
        element = '{:6}  ' if data.dtype in ['int32', 'int64'] else '{:14.6e}  '
        for i, d in enumerate(data):
            s += element.format(d)
            row_counter += 1
            if row_counter == elements_per_row and i + 1 != len(data):
                row_counter = 0
                s += '\n{}'.format(empty_card)
        s += '\n'
        return s

    def cals_divs(self):
        # calculate the midpoints of each pixel
        self.y_div = np.linspace(values.y_min, values.y_max, values.numy + 1)
        self.y_mids = (self.y_div[1:] + self.y_div[:-1]) / 2
        # repeat for z values
        self.z_div = np.linspace(values.z_min, values.z_max, values.numz + 1)
        self.z_mids = (self.z_div[1:] + self.z_div[:-1]) / 2

    def add_positions(self):
        # add Y and Z distributions
        # calculate the pixel height and width
        y_diff = (self.y_div[1] - self.y_div[0]) / 2
        z_diff = (self.z_div[1] - self.z_div[0]) / 2
        self.s += 'SI1  H  -{:.5f}   {:.5f}\n'.format(y_diff, y_diff)
        self.s += 'SP1  D 0  1\n'
        self.s += 'SI2  H  -{:.5f}   {:.5f}\n'.format(z_diff, z_diff)
        self.s += 'SP2  D 0  1\n'

        # create all of the points for the sdef
        points = []
        for i in self.y_mids:
            for j in self.z_mids:
                points.append(0.000)
                points.append(i)
                points.append(j)
        points = np.array(points)
        # add the midpoints and pdf values for each pixel
        self.s += self.card('SI3  L  ', points, 3)
        self.s += self.card('SP3     ', self.totals.flatten(), 4)

        # make quick 3d plot to check if its good
        xx, yy = np.meshgrid(self.y_mids, self.z_mids)
        fig = plt.figure(0)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, self.totals.T, cmap='plasma')
        plt.show()

        # add each energy distribution
        d = 5
        dist = np.arange(d, d+len(self.totals.T.flatten()))
        self.s += self.card('DS4  S  ', dist, 7)
        for i in range(len(self.y_mids)):
            for j in range(len(self.z_mids)):
                erg_dist = self.data[i][j]
                self.s += self.card('SI{}  H  '.format(d), self.energies, 4)
                self.s += self.card('SP{}  D  '.format(d), erg_dist, 4)
                d += 1

    def txt(self):
        ''' Write the data to a text file.'''
        with open('filtered_source.sdef', 'w+') as F:
            F.write(self.s)

    def sr(self):
        ''' Returns a string representation of the source term.'''
        return self.s

if __name__ == '__main__':
    brick = Source()
    brick.txt()
