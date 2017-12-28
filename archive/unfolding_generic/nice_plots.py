from matplotlib import rc, rcParams


class Nice_Plots(object):
    def __init__(self):
        rc('font', **{'family': 'serif'})
        rcParams['xtick.direction'] = 'out'
        rcParams['ytick.direction'] = 'out'
        rcParams['xtick.labelsize'] = 18
        rcParams['ytick.labelsize'] = 18
        rcParams['lines.linewidth'] = 1.85
        rcParams['axes.labelsize'] = 20
        rcParams.update({'figure.autolayout': True})
