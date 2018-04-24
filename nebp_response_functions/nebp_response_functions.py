import numpy as np

data = np.loadtxt('nebp_response_functions.txt').reshape(7, -1, 4)
data = data.T
c = 1.774E-2 * (1/4)
response_matrix = data[2] * c
response_matrix = response_matrix.T
