import re
import matplotlib.pyplot as plt
from spectrum import Spectrum
import numpy as np


def grab_spectrum(name):
    with open(name, 'r') as F:
        text = F.read()

    # split in to energy and values
    text = text.split('c')
    erg = text[0]
    vals = text[1]

    # pull energies
    pat = r'\d+.\d+e?-?\d*'
    pat = re.compile(pat)
    erg = pat.findall(erg)
    erg = np.array([float(i) for i in erg])

    # pull values
    pat2 = r'( 0 |[.][\d]+)'
    pat2 = re.compile(pat2)
    vals = pat2.findall(vals)
    vals = np.array([float(i) for i in vals])

    # create spectrum object
    return Spectrum(erg, vals[1:])


ambe_bare = grab_spectrum('ambe_bare.mcnpsrc')

fig = plt.figure(0)
ax = fig.add_subplot(111)
ax.set_xlabel('Energy $MeV$')
ax.set_ylabel('p(E)')
ax.plot(ambe_bare.step_x, ambe_bare.step_y, label='AmBe Neutron Spectrum', color='indigo')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, 12)
ax.text(4.1, 0.175,'AmBe Neutron Spectrum')
fig.savefig('ambe_bare.png', dpi=300)

