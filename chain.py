class args(object):
    def __init__(self, *posargs, **kwdargs):
        self.args = posargs
        self.kwds = kwdargs
        self.value = None

    def chain(self, other):
        if isinstance(other, args):
            new_args = self.args + other.args
            new_kwds = self.kwds.copy()
            new_kwds.update(other.kwds)
            res = args(*new_args, **new_kwds)
            res.value = self.value
        else:
            value = other(*self.args, **self.kwds)
            if isinstance(value, args):
                res = value
            else:
                res = args(value)
                res.value = value
        return res

    def __or__(self, other):
        return self.chain(other)


def chain(argsobj, *chain):
    for other in chain:
        argsobj = argsobj.chain(other)
    return argsobj.value
