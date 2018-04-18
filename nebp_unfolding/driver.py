from unfolding_experiment import Experiment
from uncertainty_analysis import Uncertainty_Analysis
from plotter import Plot
import time

start_time = time.time()

# Experiment()
Uncertainty_Analysis()
# Plot()

print('Unfolding Experiment Finished in {} s.'.format(time.time() - start_time))
