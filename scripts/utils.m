// Given a filename containing a key-value pair, returns an associative
// array expressing the same information as in the file.
// Assumes each key-value pair is separated by a colon, and that
// there are no duplicate keys.
function read_combinatorial_ids(fname)
    F := Read(fname);
    lines := Split(F, "\n");
    map := AssociativeArray();
    for line in lines do
        data := Split(line, ":");
        k, v := Explode(data);
        map[eval(k)] := eval(v);
    end for;
    return map;
end function;


// Returns true if there is a reflexive id in ids such that
// the reflexive Fano 3-tope with such id is affinely equivalent
// to P. If so, returns true and the matching id.
function is_equivalent_to_any(P, ids)
    assert IsFano(P);
    assert IsReflexive(P);
    for id in ids do
        Q := PolytopeReflexiveFanoDim3(id);
        if IsEquivalent(Q, P) then
            return true, id;
        end if;
    end for;
    return false;
end function;


// Returns the reflexive id for the polytope P.
// map is an associative array mapping tuples in the form
// <#vertices, #edges, #facets, #points> to a set with the
// reflexive ids that share the combinatorial properties in the key.
function reflexive_id_for_polytope(P, map)
    assert IsFano(P);
    assert IsReflexive(P);
    k := <#Vertices(P), #Edges(P), #Facets(P), #Points(P)>;
    ids := map[k];
    return is_equivalent_to_any(P, ids);
end function;

