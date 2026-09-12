import re

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class HeuristicConstructionsMixin:
    """
    The `HeuristicConstructionsMixin` contains functions for composing new SEMENTs where the specific construction is ambiguous.
    The functions will use information from the given SEMENTs to determine the correct function to use.
    For example, if a graph has an edge called "descriptor" that might point to an adjective or what would be realized as a passive participle modifier
    As far as the MRS is concerned, the composition for these is different so this function will "guess" what type of descriptor was given and proceed that way
    """


    @SemCompTracer.trace
    def quantify_generic(self, quantified_SEMENT: SEMENT) -> SEMENT:
        """
        Quantify a SEMENT in with generic quantifier, specifically `def_udef_a_q`

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `quantified_SEMENT` | `SEMENT` | SEMENT to quantify |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | Quantified SEMENT |
        """
        quant_sement = None
        # if there's an ad-hoc "QUANT" feature on the quantified_SEMENT's INDEX then use that
        if 'QUANT' in quantified_SEMENT.variables[quantified_SEMENT.index]:
            quant_sement = self.quantifier(quantified_SEMENT.variables[quantified_SEMENT.index]['QUANT'])
            # remove ad-hoc QUANT feature
            quantified_SEMENT.variables[quantified_SEMENT.index].pop('QUANT')
        else:
            for rel in quantified_SEMENT.rels:
                # if the INDEX is the ARG0 of a "card" relation then quantify ith number_q
                if rel.predicate == "card" and rel.args['ARG0'] == quantified_SEMENT.index:
                    quant_sement = self.quantifier("number_q")
                    break
                # if it's a name use the new explicit_or_proper_q abstract predicate :D
                elif (rel.predicate == "named" or rel.predicate == "named_pl") and rel.args['ARG0'] == quantified_SEMENT.index:
                    quant_sement = self.quantifier("explicit_or_proper_q")
                    break

            if quant_sement is None:
                quant_sement = self.quantifier("def_udef_a_q")

        return self.semantic_algebra.op_scopal_quantifier(quant_sement, quantified_SEMENT)

    # @SemCompTracer.trace
    # def X_of_Y_is_Z(self, X_SEMENT: SEMENT, Y_SEMENT: SEMENT, Z_SEMENT: SEMENT):
    #
    #     if not SEMENTUtil.check_if_quantified(Y_SEMENT):
    #         y_quant = self.quantify_generic(Y_SEMENT)
    #     else:
    #         y_quant = Y_SEMENT
    #
    #     # check if X_SEMENT has an ARG1 (e.g. _bag_n_of)
    #     if "ARG1" in X_SEMENT.slots:
    #         copula_subject = self.object_of_noun(X_SEMENT, y_quant)
    #     # if not, introduce "of" preposition
    #     else:
    #         of = self.preposition("of_p")
    #         of_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(of, y_quant, "ARG2")
    #         copula_subject = self.semantic_algebra.op_non_scopal_argument_hook_slots(of_ARG2_plugged, X_SEMENT, "ARG1")
    #
    #     if not SEMENTUtil.check_if_quantified(copula_subject):
    #         x_quant = self.quantify_generic(copula_subject)
    #     else:
    #         x_quant = copula_subject
    #
    #     if not SEMENTUtil.check_if_quantified(Z_SEMENT):
    #         z_quant = self.quantify_generic(Z_SEMENT)
    #     else:
    #         z_quant = Z_SEMENT
    #
    #     return self.copula(x_quant, z_quant)
    #
    # @SemCompTracer.trace
    # def X_is_Y_of_Z(self, X_SEMENT: SEMENT, Y_SEMENT: SEMENT, Z_SEMENT: SEMENT):
    #
    #     if not SEMENTUtil.check_if_quantified(Z_SEMENT):
    #         z_quant = self.quantify_generic(Z_SEMENT)
    #     else:
    #         z_quant = Z_SEMENT
    #
    #     # check if Y_SEMENT has an ARG1 (e.g. _bag_n_of)
    #     if "ARG1" in Y_SEMENT.slots:
    #         copula_object = self.object_of_noun(Y_SEMENT, z_quant)
    #     # if not, introduce "of" preposition
    #     else:
    #         of = self.preposition("of_p")
    #         of_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(of, z_quant, "ARG2")
    #         copula_object = self.semantic_algebra.op_non_scopal_argument_hook_slots(of_ARG2_plugged, Y_SEMENT, "ARG1")
    #
    #     if not SEMENTUtil.check_if_quantified(X_SEMENT):
    #         x_quant = self.quantify_generic(X_SEMENT)
    #     else:
    #         x_quant = X_SEMENT
    #
    #     if not SEMENTUtil.check_if_quantified(copula_object):
    #         y_quant = self.quantify_generic(copula_object)
    #     else:
    #         y_quant = Y_SEMENT
    #
    #     return self.copula(x_quant, y_quant)