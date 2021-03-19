This repository contains some tools written in magma that are helpful to construct a chain of reflexive Fano polytopes in 3 dimensions.

The algorithm is mostly as follows.
For every reflexive 3-tope P do the following steps:

1. For every vertex v of P:
   - construct the polytope Q obtained from P by removing the vertex v.
   - if Q is a reflexive Fano 3-tope, add it to the list of nodes, and add an edge between P and Q.
2. Make sure that there are no repeated vertices in the graph.

In the folder utils there are some python scripts that can be used to postprocess and understand the results of the computations.

