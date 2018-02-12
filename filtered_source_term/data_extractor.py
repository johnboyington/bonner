import re


class Extract(object):
    def __init__(self):
        self.load_file()
        self.split_output()
        self.write_data()

    def load_file(self):
        f = open('input.inpo', 'r')
        self.output = f.read()

    def split_output(self):
        self.output = self.output.split('PIXEL')
        self.output = self.output[85:-1]
        self.s = ''
        s = r'\d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        for block in self.output:
            values = pattern.findall(block)
            if len(values) > 0:
                self.s += str(values[-1]) + '\n'

    def write_data(self):
        with open('data.txt', 'w') as F:
            F.write(self.s)

Extract()
