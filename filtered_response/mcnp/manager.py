from sphere import Sphere
import numpy as np


class Generator(object):
    def __init__(self, test=False):
        self.nps = 1000000
        self.diameters = np.array([0, 2, 3, 5, 8, 10, 12])
        if test:
            self.test_experiment()
            pass
        else:
            self.run_experiment()

    def run_experiment(self):
        for d in self.diameters:
            sph = Sphere(d, self.nps)
            sph.run()
            out = sph.output()
            with open('filtered_responses.txt', 'a+') as F:
                F.write(out + '\n')


if __name__ == '__main__':
    generate = Generator()
