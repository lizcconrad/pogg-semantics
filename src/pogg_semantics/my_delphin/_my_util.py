# altered versions of some functions from delphin util module

from delphin import util, mrs

from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Set,
    Tuple,
    Union,
)

_IsoGraph = Dict[str, Dict[Union[None, str], str]]
_IsoMap = Dict[str, str]
_IsoPairs = List[Tuple[str, str]]

def _vf2_feasible_ignore_predicates(
        mapping: _IsoMap,
        g1: _IsoGraph,
        g2: _IsoGraph,
        n: str,
        m: str,
) -> bool:
    e1 = g1[n]  # edges from n in g1
    e2 = g2[m]  # edges from m in g2
    inv_map = {b: a for a, b in mapping.items()}  # inverse of bijection

    # semantic feasibility of nodes
    # ECC: ignore this to enable checking for "loose isomorphism"(?)
    # i.e. let two MRS structures be isomorphic even if the predicate labels don't match
    # if e1.get(None, '') != e2.get(None, ''):
    #     return False


    # accounts for r_in, r_out
    if len(e1) != len(e2):
        return False
    # accounts for r_new (only 1 extra level of lookahead)
    if (len(util._vf2_new(mapping, g1, n)) != len(util._vf2_new(inv_map, g2, m))):
        return False
    # accounts for r_pred, r_succ
    if not (util._vf2_consistent(mapping, g1, g2, n, m)
            and util._vf2_consistent(inv_map, g2, g1, m, n)):
        return False
    return True

def _vf2_ignore_predicates(g1: _IsoGraph, g2: _IsoGraph) -> _IsoMap:
    """See Cordella, Foggia, Sansone, and Vento 2004"""

    # augment graph with inverse edges, making it effectively undirected
    util._vf2_inv_map(g1)
    util._vf2_inv_map(g2)

    # VF2 is defined recursively but it is simple to make iterative
    mapping: _IsoMap = {}
    prev_n = None
    candidates = util._vf2_candidates(mapping, g1, g2)
    states: List[Tuple[Union[None, str], _IsoPairs]] = []
    while len(mapping) < len(g2):
        pair_found = False
        while candidates and not pair_found:
            n, m = candidates.pop()
            if _vf2_feasible_ignore_predicates(mapping, g1, g2, n, m):
                pair_found = True

        if pair_found:
            # make new state
            mapping[n] = m
            states.append((prev_n, candidates))
            prev_n = n
            candidates = util._vf2_candidates(mapping, g1, g2)
        elif prev_n is None:
            # end of the line; abort
            break
        else:
            # restore old state
            del mapping[prev_n]
            prev_n, candidates = states.pop()

    return mapping


def is_isomorphic_ignore_predicate_labels(m1: mrs.MRS,
                  m2: mrs.MRS,
                  properties: bool = True) -> bool:
    """
    Return `True` if *m1* and *m2* are isomorphic MRSs.

    Isomorphicity compares the predicates of a semantic structure, the
    morphosemantic properties of their predications (if
    `properties=True`), constant arguments, and the argument structure
    between predications. Non-semantic properties like identifiers and
    surface alignments are ignored.

    Args:
        m1: the left MRS to compare
        m2: the right MRS to compare
        properties: if `True`, ensure variable properties are
            equal for mapped predications
    """
    # simple tests
    if (len(m1.rels) != len(m2.rels)
            or len(m1.hcons) != len(m2.hcons)
            or len(m1.icons) != len(m2.icons)
            or len(m1.variables) != len(m2.variables)):
        return False

    g1 = mrs._operations._make_mrs_isograph(m1, properties)
    g2 = mrs._operations._make_mrs_isograph(m2, properties)

    iso = _vf2_ignore_predicates(g1, g2)
    return set(iso) == set(g1)
