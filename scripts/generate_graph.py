""" This script generates all graphs that can be obtained
    from a reflexive Fano 3-tope by removing one vertex
    from it at a time.
    After collecting all the results, the complete graphs
    are saved in the file data/r3_graphs.txt
"""
from queue import Queue
import subprocess
from threading import Thread
from utils import process_magma_output, read_polytope_ids


# How many tasks to run concurrently.
n_workers = 4


def magma_worker(queue, seen, Gs):
    """ Launches a magma process and parses its results. """
    while True:
        try:
            n = queue.get()
        except queue.Empty:
            print("All done.")
            return
        else:
            cmd = ["magma", "-b", f"rid:={n}", "generate_graph.m"]
            res = subprocess.run(cmd, capture_output=True)
            graph = process_magma_output(res.stdout)
# Update the ids seen so far.
            seen |= graph.keys()
            Gs.append(graph)


if __name__ == "__main__":
    pids = read_polytope_ids()
# Keep track of the polytopes already seen in some graph.
    seen = set()
# List with the graphs for all the reflexive 3-topes.
    Gs = []
    q = Queue(maxsize=n_workers)
    threads = [Thread(target=magma_worker, args=(q, seen, Gs)) for _ in range(n_workers)]
    [t.start() for t in threads]
# We parse the database from the polytopes with more
# points to the polytopes with fewer points.
    for k in sorted(pids.keys(), reverse=True):
        for n in pids[k]:
            if n not in seen:
                q.put(n)

    with open("../data/r3_graphs.txt", "w") as fw:
        for G in Gs:
            for k, v in G.items():
                fw.write(f"{k}: {v}\n")
            fw.write("\n")

    print("All done.")

