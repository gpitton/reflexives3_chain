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

