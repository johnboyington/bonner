from unfolding_experiment import Experiment
from plotter import Plot
import time

start_time = time.time()

Experiment()
# Plot()

print('Unfolding Experiment Finished in {} s.'.format(time.time() - start_time))
