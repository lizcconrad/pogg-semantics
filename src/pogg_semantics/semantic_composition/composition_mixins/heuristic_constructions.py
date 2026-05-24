from pogg.my_delphin.my_delphin import SEMENT
import re
from delphin import ace
from pogg.my_delphin import sementcodecs
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

from pogg.semantic_composition.call_tracer import SemCompTracer

class HeuristicConstructionsMixin:
    """
    The `HeuristicConstructionsMixin` contains functions for composing new SEMENTs where the specific construction is ambiguous.
    The functions will use information from the given SEMENTs to determine the correct function to use.
    For example, if a graph has an edge called "descriptor" that might point to an adjective or what would be realized as a passive participle modifier
    As far as the MRS is concerned, the composition for these is different so this function will "guess" what type of descriptor was given and proceed that way
    """

    @SemCompTracer.trace
    def generic_prenominal_descriptor(self, descriptor_SEMENT: SEMENT, described_SEMENT: SEMENT) -> SEMENT:
        # edges labeled "descriptor" may have an adjective or a participle as their child
        # so the function has to determine which type of descriptor it has and do composition based on that

        descriptor_key_rel = POGGSEMENTUtil.get_key_rel(descriptor_SEMENT)

        # if the descriptor's key_rel is a verb...
        if re.match(r"_[a-z]+_v_", descriptor_key_rel.predicate):
            # if there's an ARG2, use a passive participle (e.g. 'the broken window')
            if 'ARG2' in descriptor_key_rel.args:
                return self.passive_participle_modifier(descriptor_SEMENT, described_SEMENT)
            # if there's no ARG2, use a present participle (e.g. 'the glowing flower')
            else:
                result = self.present_participle_modifier(descriptor_SEMENT, described_SEMENT)
                return result
        # if the descriptor's key_rel is a noun, treat it like a compound
        elif re.match(r"_[a-z]+_n_", descriptor_key_rel.predicate):
            return self.compound_noun(described_SEMENT, descriptor_SEMENT)
        # assume it's an adjective otherwise
        else:
            # if the thing being described is a proper noun, give the adjective's intrinsic variable TENSE information
            # then we get "Liz, who is happy" instead of "happy Liz"
            described_key_rel = POGGSEMENTUtil.get_key_rel(described_SEMENT)
            if described_key_rel.predicate == 'named':
                return self.nonrestrictive_adjectival_relative_clause(descriptor_SEMENT, described_SEMENT)
            else:
                return self.prenominal_adjective(descriptor_SEMENT, described_SEMENT)

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
        for rel in quantified_SEMENT.rels:
            # if the INDEX is the ARG0 of a "named" relation then quantify with def_or_proper_q
            # if rel.predicate == "named" and rel.args['ARG0'] == quantified_SEMENT.index:
            #     quant_sement = self.quantifier("def_or_proper_q")
            #     break
            # if the INDEX is the ARG0 of a "card" relation then quantify ith number_q
            if rel.predicate == "card" and rel.args['ARG0'] == quantified_SEMENT.index:
                quant_sement = self.quanitifier("number_q")
                break

        if quant_sement is None:
            quant_sement = self.quantifier("def_udef_a_q")

        return self.semantic_algebra.op_scopal_quantifier(quant_sement, quantified_SEMENT)
