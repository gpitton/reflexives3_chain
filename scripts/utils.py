from collections import defaultdict


def process_magma_output(bstdout):
    """ Builds the graph implied from magma's output. """
    stdout = bstdout.decode("utf-8")
    lines = stdout.rstrip("\r\n").split("\n")
    graph = dict()
    for line in lines:
        s = line.split(":")
        graph[int(s[0])] = eval(s[1])
    return graph


def read_polytope_ids(fname="../data/r3_cdata.txt"):
    """ Returns an associative array mapping a positive integer n
        to the set of all reflexive Fano ids with n lattice points.
    """
    fano_ids = defaultdict(set)
    with open(fname, "r") as f:
        for l in f:
            s = l.split(":")
            ns = eval("[" + s[0][1:-1] + "]")
            n = ns[3]
            ids = eval(s[1])
            fano_ids[n] |= ids
    return fano_ids


class hashdict(dict):
    """ A class useful to realise an immutable, hashable dictionary.
        Note that immutability is not enforced.
    """
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self._data = ((k, v) for k, v in self.items())

    def __hash__(self):
        return hash(self._data)

    def __eq__(self, other):
        if isinstance(other, hashdict):
            return self._data == other._data
        else:
            raise NotImplemented

