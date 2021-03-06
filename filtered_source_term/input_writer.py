import values
import numpy as np


class Write(object):
    def __init__(self):
        self.energies = values.energies
        self.template = self.load_data()
        self.make_surfs()
        self.make_cells()
        self.make_imp()
        self.make_tallies()
        self.write_input()

    def load_data(self):
        f = open('filter.tem', 'r')
        template = f.read()
        return template.split('*FLAG*')

    def make_surfs(self):
        y_init = 200
        z_init = 300
        y_div = np.linspace(values.y_min, values.y_max, values.numy + 1)
        self.y_s = ''
        self.y_data = []
        for i, y in enumerate(y_div):
            self.y_data += [(i + y_init, y)]
            self.y_s += '{} PY {:9.6f}\n'.format(i + y_init, y)
        z_div = np.linspace(values.z_min, values.z_max, values.numz + 1)
        self.z_s = ''
        self.z_data = []
        for i, z in enumerate(z_div):
            self.z_data += [(i + z_init, z)]
            self.z_s += '{} PZ {:9.6f}\n'.format(i + z_init, z)

    def make_cells(self):
        n = 300
        self.cell_s = ''
        for i, y in enumerate(self.y_data[:-1]):
            for j, z in enumerate(self.z_data[:-1]):
                form = n, self.y_data[i][0], self.y_data[i+1][0],  self.z_data[j][0], self.z_data[j+1][0]
                self.cell_s += '{} 0 133 -32  {}  -{}   {}  -{} \n'.format(*form)
                n += 1
        # add filter slabs
        form = self.y_data[0][0], self.y_data[-1][0],  self.z_data[0][0], self.z_data[-1][0]
        self.cell_s += '200  4  -8.65000 {} -{} {} -{}  130 -131   $ Cadmium\n'.format(*form)
        self.cell_s += '201  1  -1.00000 {} -{} {} -{}  131 -132   $ Borated Polyethylene\n'.format(*form)
        self.cell_s += '204  2 -11.34000 {} -{} {} -{}  132 -133   $ Lead\n'.format(*form)
        # add problem space cell operators
        form = self.y_data[0][0], self.y_data[-1][0],  self.z_data[0][0], self.z_data[-1][0]
        ps = '90 0  -32 (130 -32 -{}):(130 -32 {}):(130 -32 -{}):(130 -32 {})'.format(*form)
        ps2 = '91 0 -130 -32'
        self.cell_s += 'c\n{}\nc\n{}\nc\n'.format(ps, ps2)

    def make_imp(self):
        n = 4 + (values.numy)*(values.numz)
        self.imp_s = 'IMP:n 1 {}r 0\nIMP:p 1 {}r 0\n'.format(n, n)

    def make_tallies(self):
        n = 300
        self.tally_s = ''
        e_string = self.string_energies(self.energies)
        for i, y in enumerate(self.y_data[:-1]):
            for j, z in enumerate(self.z_data[:-1]):
                form = n, self.y_data[i][0], self.y_data[i+1][0],  self.z_data[j][0], self.z_data[j+1][0]
                self.tally_s += 'F{}1:n 133\n'.format(n)
                self.tally_s += 'FS{}1    -{}  {}   -{}  {} \n'.format(*form)
                self.tally_s += 'E{}1    {}\n'.format(n, e_string)
                self.tally_s += 'FC{}1 PIXEL{}\n'.format(n, n)
                n += 1

    def string_energies(self, bins):
        n = 1
        s = ''
        for e in bins:
            s += '{:9.6e}  '.format(e)
            if not n % 4:
                s += '\n        '
            n += 1
        return s

    def write_input(self):
        self.inp = self.template[0]
        self.inp += self.cell_s
        self.inp += self.template[1]
        self.inp += self.y_s
        self.inp += self.template[2]
        self.inp += self.z_s
        self.inp += self.template[3]
        self.inp += self.imp_s
        self.inp += self.template[4]
        self.inp += self.tally_s
        self.inp += self.template[5]
        with open('data/input.inp', 'w') as F:
            F.write(self.inp)


Write()
