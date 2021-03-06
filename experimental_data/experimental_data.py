import numpy as np
import ambe_calibration
import matplotlib.pyplot as plt


class Bonner_Data(object):

    def __init__(self, filename, background, t=300, p=25):
        self.t = t  # counting time - the total time (s) of the measurement
        self.p = p  # power - the power W(th) of the measurement
        # load in data
        data = np.loadtxt(filename, skiprows=2)
        # subtract the error
        data = self.sub_error(data, background)
        # normalize the data
        data = self.normalize(data)

        # divide data into values and error
        self.values = data[0]
        self.error = data[1]

    def normalize(self, data):
        ''' Normalize a given data set using the following parameters '''
        # parameters
        e = ambe_calibration.detection_efficiency  # detector efficiency - the efficiency of the bonner cart's LiI detector
        self.pf = 250 / self.p  # power factor - ratio of desired power to power which measurements were taken

        # multiply data by coefficients
        data *= (1/e)
        data *= (1/self.t)
        data *= self.pf

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
bg = np.loadtxt('/home/john/workspace/bonner/experimental_data/2_background.txt', skiprows=2)
bg3 = bg * (12/5)  # multiply previous bg count to be in the same timescale as filtered3

# load in experimental datasets
# unfiltered response from first experiment
unfiltered1 = Bonner_Data('/home/john/workspace/bonner/experimental_data/1_responses_unfiltered.txt', bg)
# unfiltered response from second experiment
unfiltered2 = Bonner_Data('/home/john/workspace/bonner/experimental_data/2_responses_unfiltered.txt', bg)
# filtered response from second experiment
filtered2 = Bonner_Data('/home/john/workspace/bonner/experimental_data/2_responses_filtered.txt', bg)
# filtered response from second experiment
filtered3 = Bonner_Data('/home/john/workspace/bonner/experimental_data/3_responses_filtered.txt', bg3, 12*60, 250)

if False:
    plt.errorbar(range(7), filtered2.values, filtered2.error)
    plt.errorbar(range(7), filtered3.values, filtered3.error)
