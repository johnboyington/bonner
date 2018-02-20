from source_writer import Source

with open('test.temp', 'r') as F:
    template = F.read()
src = Source()

test = template + src.sr()

with open('test.i', 'w+') as F:
    F.write(test)
