from itertools import repeat
from random import randrange


def randoms_from(values, length=None):
    _range = range(length) if length is not None else repeat(0)
    values_len = len(values)
    for _ in _range:
        yield values[randrange(0, values_len)]
