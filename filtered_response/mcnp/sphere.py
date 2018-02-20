import os
from source_writer import Source
src = Source()


class Sphere(object):

    def __init__(self, size, particles):
        self.size = size * (2.54 / 2)
        self.particles = particles
        self.response = (0, 0)

    def write(self):
        default_text = open('cards.txt', 'r').read().split('*FLAG*')
        s = default_text[0]
        for sphere in range(7):
            s += '{}  SO  {}    \n'.format(sphere + 1, self.size * ((sphere + 1) / 7))
        s += default_text[1]
        s += 'NPS   {}\n'.format(self.particles)
        s += src.sr()
        s += default_text[2]
        with open('sphere.i', 'w+') as F:
            F.write(s)
        return

    def extract(self):
        F = open('sphere.io', 'r').readlines()
        for ii in range(len(F)):
            if ' multiplier bin:   1.00000E+00         2         105' in F[ii]:
                line = F[ii + 1]
                val = float(line[17:28])
                err = float(line[29:35])
                return val, err

    def run(self, clean=True):
        self.write()
        os.system('mcnp6 name=sphere.i tasks 26')
        self.response = self.extract()
        if clean:
            os.remove('sphere.i')
            os.remove('sphere.io')
            os.remove('sphere.ir')
        return self.response

    def output(self):
        args = int(round(self.size * (2 / 2.54))), self.response[0], self.response[1]
        return '{:2d}   {:14.8e}   {:14.8e}'.format(*args)


if __name__ == '__main__':
    sp = Sphere(1, 0.5, 1, [-1, 0, 1], [0, 0.01, 0.99], 100000)
    sp.run()
    print(sp.output())
