import numpy as np
from spectrum import Spectrum


edges = np.loadtxt('/home/john/workspace/bonner/nebp_unfolding/scale56.txt')


def load_dataset(name):
    data = np.loadtxt('/home/john/workspace/bonner/nebp_unfolding/data/{}_unfolded.txt'.format(name))
    data = data.T
    return Spectrum(edges, data[1], data[2], dfde=True)

# load unfolded data
unfolded_data = {}
datasets = ['e1_ne_gr', 'e1_ne_mx',
            'e2_ne_gr', 'e2_ne_mx',
            'f2_ne_gr', 'f2_ne_mx',
            'f2_fi_gr', 'f2_fi_mx',
            'f2_un_gr', 'f2_un_mx',
            'f3_ne_gr', 'f3_ne_mx',
            'f3_fi_gr', 'f3_fi_mx',
            'f3_un_gr', 'f3_un_mx']

for name in datasets:
    unfolded_data['{}'.format(name)] = load_dataset(name)
