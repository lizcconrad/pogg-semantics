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


    @SemCompTracer.trace
    def modifier_generic(self, modifier_SEMENT: SEMENT, modified_SEMENT: SEMENT) -> SEMENT:

        modifier_key_rel = SEMENTUtil.get_key_rel(modifier_SEMENT)

        # if top level index is e and pred specifies _a_ or _v_
        if (modifier_SEMENT.index.startswith("e") or
                ("_a_" in modifier_key_rel.predicate or "_v_" in modifier_key_rel.predicate)):
            # adjective?
            if "_a_" in modifier_key_rel.predicate:
                return self.adjective_as_modifier(modifier_SEMENT, modified_SEMENT)
            # something else?
            else:
                # fill the highest slot
                try:
                    highest_slot = sorted(modifier_SEMENT.slots.keys())[-1]
                except IndexError:
                    raise IndexError("No slots available to fill for generic modifier")


                if highest_slot == "ARG3":
                    # if the key_rel has more than 3 ARGs, one has been filled so use relative
                    if len(modifier_key_rel.args.keys()) > 4:
                        return self.relative_predicate_and_oblique(modifier_SEMENT, modified_SEMENT)
                    else:
                        return self.modifying_participle_and_oblique(modifier_SEMENT, modified_SEMENT)
                elif highest_slot == "ARG2":
                    # if the key_rel has more than 2 ARGs, one has been filled so use relative
                    if len(modifier_key_rel.args.keys()) > 3:
                        return self.relative_predicate_and_proto_patient(modifier_SEMENT, modified_SEMENT)
                    else:
                        return self.modifying_participle_and_proto_patient(modifier_SEMENT, modified_SEMENT)
                else:
                    # if the key_rel has more than 2 ARGs, one has been filled so use relative
                    if len(modifier_key_rel.args.keys()) > 2:
                        return self.relative_predicate_and_proto_agent(modifier_SEMENT, modified_SEMENT)
                    else:
                        return self.modifying_participle_and_proto_agent(modifier_SEMENT, modified_SEMENT)
        else:
            # if key_rel of modifier is _n_, do compound noun, otherwise compound generic
            if "_n_" in modifier_key_rel.predicate:
                return self.compound_noun(modified_SEMENT, modifier_SEMENT)
            else:
                return self.compound_generic(modified_SEMENT, modifier_SEMENT)