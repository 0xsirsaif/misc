import timeit

TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤'
def non_ascii(c):
    return c > 127
"""


def clock(label, cmd):
    """
    timeit.repeat() returns a list of 3 timings: best, average, worst
    cmd is the command to be timed
    the setup is run once, then the command is run TIMES times
    number is the number of times to run the command
    """
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES)
    print(label, *(f'{x:.3f}' for x in res))


clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]


def nested_unpacking():
    print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
    fmt = '{:15} | {:9.4f} | {:9.4f}'
    # _ is a throwaway variable. TODO: loop variable could have the same name. the last one wins
    for name, _, _, (latitude, longitude) in metro_areas:
        if longitude <= 0:
            print(fmt.format(name, latitude, longitude))


nested_unpacking()
