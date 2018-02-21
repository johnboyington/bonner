import numpy as np


def normalize(data):
    ''' Normalize a given data set using the following parameters '''
    # parameters
    e = 1  # detector efficiency - the efficiency of the bonner cart's LiI detector
    t = 5 * 60  # counting time - the total time (s) of the measurement
    pf = 250 / 25  # power factor - ratio of desired power to power which measurements were taken

    # multiply data by coefficients
    data *= (1/e)
    data *= (1/t)
    data *= pf

    # return normalized data
    return data


def sub_error(counts_gross, bg):
    ''' Subtract calculate the error and propogate through background subtraction '''
    # calculate absolute errors
    error = np.sqrt(counts_gross)
    bg_error = np.sqrt(bg)

    # subtract background
    counts_net = counts_gross - bg
    error_net = np.sqrt(error**2 + bg_error**2)

    return np.array([counts_net, error_net])


def save(i, o, bg):
    ''' Control the input and output of the data '''
    # load in data
    data = np.loadtxt(i, skiprows=2)
    # subtract the error
    data = sub_error(data, bg)
    # normalize the data
    data = normalize(data)
    # save under the given name
    np.savetxt(o, data)


# load in background data
bg = np.loadtxt('2_background.txt', skiprows=2)

# load in experimental datasets
save('1_responses_unfiltered.txt', 'e1u.nr', bg)
save('2_responses_unfiltered.txt', 'e2u.nr', bg)
save('2_responses_filtered.txt', 'e2f.nr', bg)
