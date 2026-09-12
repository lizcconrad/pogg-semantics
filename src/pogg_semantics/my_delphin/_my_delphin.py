"""
This module consists of the `SEMENT` class, which is a subclass of `delphin.mrs.MRS`.

[See usage examples here.](project:/usage_nbs/pogg/my_delphin/my_delphin_usage.ipynb)
"""

# modified versions of pydelphin elements that may be submitted for a PR later
# taken from the _mrs.py file to test my subclass
from typing import Optional, Iterable, Mapping

import delphin.semi
from delphin.lnk import Lnk
# end from _mrs.py

from copy import deepcopy
from delphin import mrs


class SEMENT(mrs.MRS):
    """
    A SEMENT (Semantic Element) is formally very similar to an MRS (Minimal Recursion Semantics) structure but with additional machinery to enable composition.


    An MRS is typically understood to be a "complete" structure which will not participate in further semantic composition.
    In order to facilitate composition, a SEMENT has everything that an MRS does plus

    1. a list of "slots" (semantic arguments available to be filled, such as the SLEEPER (`ARG1`) for the verb *sleep*).
    2. a running list of equalities between variables which will be collapsed when composition is complete.
    """

    # TODO: rels, hcons, and icons are of type mrs.EP, mrs.HCons, and mrs.ICons ...
    #  should just be EP, HCons, and ICons but this isn't in the real file yet
    def __init__(self,
                 top: Optional[str] = None,
                 index: Optional[str] = None,
                 rels: Optional[Iterable[mrs.EP]] = None,
                 slots: Optional[Mapping[str, str]] = None,
                 eqs: Optional[Iterable[set[str, ...]]] = None,
                 hcons: Optional[Iterable[mrs.HCons]] = None,
                 icons: Optional[Iterable[mrs.ICons]] = None,
                 variables: Optional[Mapping[str, Mapping[str, str]]] = None,

                 # TODO: potentially temporary raising/control attributes
                 embedded_slots: Optional[Mapping[str, str]] = None,
                 # embedder_slot: Optional[Mapping[str, str]] = None,

                 lnk: Optional[Lnk] = None,
                 surface=None,
                 identifier=None):
        """
        Initialize a SEMENT object.

        **Parameters / Instance Attributes**

        Each parameter may also be accessed as an instance attribute.

        | Parameter | Type | Description |
        | --------- | ---- | ------------ |
        | `top` | `str` | top handle |
        | `index` | `str` | index variable |
        | `rels` | `Iterable[mrs.EP]` | list of EPs |
        | `slots` | `Mapping[str, Mapping[str, str]]` | dict of slots and their values |
        | `eqs` | `Iterable[set[mrs.EP]]` | list of equalities between variables |
        | `hcons` | `Iterable[mrs.HCons]` | list of handle constraints |
        | `icons` | `Iterable[mrs.ICons]` | list of ICons |
        | `variables` | `Mapping[str, Mapping[str, str]]` | dict of variables and their properties |
        """

        # this is required for control constructions because I use the same SEMENT for composition twice
        unique_rels = []
        for rel in rels:
            unique_flag = True
            for unique_rel in unique_rels:
                if rel.predicate == unique_rel.predicate:
                    if rel.args == unique_rel.args:
                        unique_flag = False
            if unique_flag:
                unique_rels.append(rel)

        super().__init__(top, index, unique_rels, hcons, icons, variables, lnk, surface, identifier)

        self.slots = slots
        self.eqs = eqs

        self.embedded_slots = embedded_slots
        # self.embedder_slot = embedder_slot