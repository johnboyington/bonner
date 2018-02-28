import numpy as np
import ambe_calibration


class Bonner_Data(object):

    def __init__(self, filename, background):
        # load in data
        data = np.loadtxt(filename, skiprows=2)
        # subtract the error
        data = self.sub_error(data, bg)
        # normalize the data
        data = self.normalize(data)

        # divide data into values and error
        self.values = data[0]
        self.error = data[1]

    def normalize(self, data):
        ''' Normalize a given data set using the following parameters '''
        # parameters
        e = ambe_calibration.detection_efficiency  # detector efficiency - the efficiency of the bonner cart's LiI detector
        t = 5 * 60  # counting time - the total time (s) of the measurement
        pf = 250 / 25  # power factor - ratio of desired power to power which measurements were taken

        # multiply data by coefficients
        data *= (1/e)
        data *= (1/t)
        data *= pf

        # return normalized data
        return data

    def sub_error(self, counts_gross, bg):
        ''' Calculate the error, and propogate through background subtraction '''
        # calculate absolute errors
        error = np.sqrt(counts_gross)
        bg_error = np.sqrt(bg)

        # subtract background
        counts_net = counts_gross - bg
        error_net = np.sqrt(error**2 + bg_error**2)

        return np.array([counts_net, error_net])


# load in background data
bg = np.loadtxt('2_background.txt', skiprows=2)

# load in experimental datasets
unfiltered1 = Bonner_Data('1_responses_unfiltered.txt', bg)  # unfiltered response from first experiment
unfiltered2 = Bonner_Data('2_responses_unfiltered.txt', bg)  # unfiltered response from second experiment
filtered2 = Bonner_Data('2_responses_filtered.txt', bg)  # filtered response from second experiment
