from collections import defaultdict, UserDict
from functools import reduce
from operator import xor


def process_magma_output(bstdout):
    """ Builds the graph implied from magma's output. """
    stdout = bstdout.decode("utf-8")
    magout = stdout.rstrip("\r\n").split("\n")
    lines = [magout[0]]
# Check if we need to merge slash-separated lines.
    append_next = False
    for line in magout[1:]:
        if append_next:
            lines[-1] += line
            append_next = False
            continue
        if line[-1] == "\\":
            append_next = True
            lines.append(line[:-1])
        else:
            lines.append(line)

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


class hashdict(UserDict):
    """ A class useful to realise an immutable, hashable dictionary.
        Note that immutability is not enforced.
    """
    def __init__(self, dictionary):
        super().__init__(dictionary)

    def __hash__(self):
        return reduce(xor, (hash(k) ^ hash(frozenset(v)) for k, v in self.data.items()))

    def __eq__(self, other):
        if isinstance(other, hashdict):
            return self.data == other.data
        else:
            raise NotImplemented

