// Remove one element at a time from every reflexive Fano 3-tope P,
// and try to build a graph connecting all reflexive 3-topes
// that can be reached by removing one or more vertices from P.
import "utils.m": reflexive_id_for_polytope, is_equivalent_to_any,
    read_combinatorial_ids;


// We assume the called will execute this script with:
// magma -b rid:=<some int> generate_graph.m
r_id := StringToInteger(rid);

// Read a pre-computed map from <#vertices, #edges, #facets, #points>
// to a reflexive id (useful for fast reverse searches).
comb_db := read_combinatorial_ids("../data/r3_cdata.txt");



// Vertices of the graph.
Vs := [Integers() | ];
// Edges of the graph. Maps a vertex id to a set of neighbours.
// The edges are directed from a polytope P to a polytope
// with one vertex less than P.
Es := AssociativeArray(Integers());
Es[r_id] := {Integers() | };

// Queue with the polytopes yet to consider.
queue := [Integers() | r_id];

while #queue gt 0 do
    m := queue[1];
    P := PolytopeReflexiveFanoDim3(m);
    vs := Vertices(P);
    for v in vs do
        vsnew := Exclude(vs, v);
        Q := Polytope(vsnew);
        if IsFano(Q) and IsReflexive(Q) then
            // We do not need to check the dimension.
            ok, n := reflexive_id_for_polytope(Q, comb_db);
            assert ok;
            if is_equivalent_to_any(Q, Vs) then
                Include(~Es[m], n);
            else
                if n in Vs then
                    Include(~Es[m], n);
                else
                    // Invariant: if n is in Vs, then n is also in Es.
                    Append(~queue, n);
                    Append(~Vs, n);
                    Include(~Es[m], n);
                    Es[n] := {Integers() | };
                end if;
            end if;
        end if;
    end for;
    Exclude(~queue, m);
end while;

for id -> e in Es do
    printf "%o: %o\n", id, ToString(e);
end for;

quit;

