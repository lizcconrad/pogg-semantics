"""
The `coordination_constructions` module contains the Mixin class for composing SEMENTs involving coordination

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class CoordinationConstructionsMixin:
    """
    The `IdiosyncraticConstructionsMixin` contains functions for composing that involve coordination
    """

    # TODO: maybe would like a better way to flag unpackable arguments than just _args but whatever
    @SemCompTracer.trace
    def coordination(self, conjunction_SEMENT: SEMENT, *coordinand_args: SEMENT) -> SEMENT:
        # the given conjunction should be used first and if there's more than 2 coordinands then implicit_conj should be used
        # so set this to true after the first coordination
        given_conj_used = False

        # start with the final coordinand
        if not SEMENTUtil.check_if_quantified(coordinand_args[-1]):
            current_SEMENT = self.quantify_generic(coordinand_args[-1])
        else:
            current_SEMENT = coordinand_args[-1]

        # go through coordinands in reverse order, starting with second to last
        for coordinand in reversed(coordinand_args[:-1]):
            if not SEMENTUtil.check_if_quantified(coordinand):
                quant_coordinand = self.quantify_generic(coordinand)
            else:
                quant_coordinand = coordinand

            if not given_conj_used:
                current_SEMENT = self.semantic_algebra.op_non_scopal_functor_hook_slots(conjunction_SEMENT,
                                                                                        current_SEMENT, "ARG2")
                current_SEMENT = self.semantic_algebra.op_non_scopal_functor_hook_slots(current_SEMENT,
                                                                                        quant_coordinand, "ARG1")
                given_conj_used = True
            else:
                implicit_conj = self.conjunction("implicit_conj")
                current_SEMENT = self.semantic_algebra.op_non_scopal_functor_hook_slots(implicit_conj, current_SEMENT,
                                                                                        "ARG2")
                current_SEMENT = self.semantic_algebra.op_non_scopal_functor_hook_slots(current_SEMENT,
                                                                                        quant_coordinand, "ARG1")

            # quantify with udef_q
            current_SEMENT = self.quantify(self.quantifier("udef_q"), current_SEMENT)

        return current_SEMENT