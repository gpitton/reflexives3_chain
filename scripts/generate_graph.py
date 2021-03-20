""" This script generates all graphs that can be obtained
    from a reflexive Fano 3-tope by removing one vertex
    from it at a time.
    After collecting all the results, the complete graphs
    are saved in the file data/r3_graphs.txt
"""
import queue
from queue import Queue
import subprocess
from threading import Thread
from utils import hashdict, process_magma_output, \
    read_polytope_ids


# How many tasks to run concurrently.
n_workers = 4


def magma_worker(q, seen, Gs):
    """ Launches a magma process and parses its results. """
    while True:
        try:
            print("here!")
            n = q.get()
            print("got",n)
        except queue.Empty:
            return
        else:
            cmd = ["magma", "-b", f"rid:={n}", "generate_graph.m"]
            res = subprocess.run(cmd, capture_output=True)
            graph = process_magma_output(res.stdout)
# Update the ids seen so far.
# Important: the next three lines should not be replaced by:
#    seen |= graph.keys(), as this would not be atomic.
            newkeys = graph.keys() - seen
            for k in newkeys:
                seen.add(k) # All is fine: add is atomic.
# We need to make the dictionary hashable to store it in a set.
            imm_graph = hashdict(graph)
            Gs.add(imm_graph)
            q.task_done()


if __name__ == "__main__":
    pids = read_polytope_ids()
# Keep track of the polytopes already seen in some graph.
    seen = set()
# Set with the graphs for all the reflexive 3-topes.
    Gs = set()
    q = Queue(maxsize=n_workers)
    threads = [Thread(target=magma_worker, args=(q, seen, Gs), daemon=True) for _ in range(n_workers)]
    [t.start() for t in threads]
# We parse the database from the polytopes with more
# points to the polytopes with fewer points.
    for k in sorted(pids.keys(), reverse=True):
        for n in pids[k]:
            if n not in seen:
                q.put(n)

    q.join()

    with open("../data/r3_graphs.txt", "w") as fw:
        for G in Gs:
            for k, v in G.items():
                fw.write(f"{k}: {v}\n")
            fw.write("\n")

    print("All done.")

