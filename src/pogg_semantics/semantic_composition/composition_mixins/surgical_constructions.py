"""
The `base_constructions` module contains the Mixin class for creating SEMENTs from a number of "basic" constructions of English.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class SurgicalConstructionsMixin:
    """
    The `SurgicalConstructionsMixin` contains functions for composing new SEMENTs using two input SEMENTs.
    """

    @SemCompTracer.trace
    def compose_propositions_via_relativization(self, matrix_SEMENT: SEMENT, relativized_SEMENT: SEMENT, slot_label: str, distinguished_rel_ARG: str) -> SEMENT:
        # collapse to simplify surgery lol
        collapsed_matrix = SEMENTUtil.overwrite_eqs(matrix_SEMENT)
        collapsed_relative = SEMENTUtil.overwrite_eqs(relativized_SEMENT)
        # hacky but whatever
        collapsed_matrix.eqs, collapsed_relative.eqs = [], []

        key_relativized_rel = SEMENTUtil.get_key_rel(collapsed_relative)
        distinguished_var = key_relativized_rel.args[distinguished_rel_ARG]
        # get the LBL for the predication whose ARG0 is the distinguished_var
        for rel in collapsed_relative.rels:
            if rel.iv == distinguished_var and not (rel.predicate.endswith("_q") or rel.predicate.endswith("_q_i")):
                disinguished_lbl = rel.label
                break

        # perform non_scopal composition as normal
        matrix_slot_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(collapsed_matrix, collapsed_relative, slot_label)
        # the new SEMENT now has two EQs that need to be changed:
        # 1. matrix_key_rel.plugged_slot = relativized_SEMENT.index ... needs to be matrix_key_rel.plugged_slot = distinguished_var
        # e.g. eat.ARG2 = tasty.ARG0 needs to be changed to eat.ARG2 = cake.ARG0
        # 2. matrix_key_rel.LBL = relativized_SEMENT.top ... needs to be relativized_SEMENT.top = distinguished_rel_ARG.LBL
        # e.g. eat.LBL = tasty.LBL ... needs to be tasty.LBL = cake.LBL
        new_eqs = []
        for eq in matrix_slot_plugged.eqs:
            if collapsed_relative.index in eq:
                new_tuple = list(eq)
                new_tuple.remove(collapsed_relative.index)
                new_tuple.append(distinguished_var)
                new_eqs.append(tuple(new_tuple))
            elif collapsed_relative.top in eq:
                new_tuple = list(eq)
                new_tuple.remove(matrix_slot_plugged.top)
                new_tuple.append(disinguished_lbl)
                new_eqs.append(tuple(new_tuple))
            else:
                pass


        matrix_slot_plugged.eqs = new_eqs
        return matrix_slot_plugged
