import values
import re


class Extract(object):
    def __init__(self):
        self.energies = values.energies
        self.load_file()
        self.split_output()
        self.write_data()

    def load_file(self):
        f = open('input.inpo', 'r')
        self.output = f.read()

    def split_output(self):
        self.output = self.output.split('PIXEL')
        num = (values.numy * values.numz) + 4
        self.output = self.output[num:-1]
        self.s = ''
        s = r'\d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        for block in self.output:
            vals = pattern.findall(block)
            vals = vals[-len(self.energies):]
            for v in vals:
                self.s += str(v) + '\n'

    def write_data(self):
        with open('data.txt', 'w') as F:
            F.write(self.s)

Extract()
