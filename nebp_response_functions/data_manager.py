from sphere import Sphere
import numpy as np


class Generator(object):
    def __init__(self, test=False):
        self.nps = 1000000
        self.diameters = np.array([0, 2, 3, 5, 8, 10, 12])
        self.angles = np.cos(np.array([90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2, 1, 0.5, 0]) * (np.pi / 180))
        self.ang_dist = None
        self.set_groups()
        if test:
            self.test_experiment()
            pass
        else:
            self.run_experiment()

    def set_groups(self):
        # all but lowest group -> [:, 1:, :]
        self.data = np.loadtxt('nebp_neutron_data.txt').reshape(len(self.angles), -1, 3)
        self.groups = self.data[0].T[0]

    def set_angular_dist(self, group):
        dist = []
        for c_bin in self.data:
            dist.append(c_bin[group][1])
        self.ang_dist = np.array(dist)

    def run_experiment(self):
        for d in self.diameters:
            for e in range(len(self.groups) - 1):
                self.set_angular_dist(e+1)
                sph = Sphere(d, self.groups[e], self.groups[e+1], self.angles, self.ang_dist, self.nps)
                sph.run()
                out = sph.output()
                with open('nebp_response_functions.txt', 'a+') as F:
                    F.write(out + '\n')

    def test_experiment(self):
        self.nps = 100000
        self.diameters = np.array([0, 2, 3])
        self.groups = self.groups[0:3]
        for d in self.diameters:
            for e in range(len(self.groups) - 1):
                self.set_angular_dist(e+1)
                sph = Sphere(d, self.groups[e], self.groups[e+1], self.angles, self.ang_dist, self.nps)
                sph.run()
                out = sph.output()
                with open('nebp_response_functions_test.txt', 'a+') as F:
                    F.write(out + '\n')


if __name__ == '__main__':
    generate = Generator()
