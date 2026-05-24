from pogg.my_delphin.my_delphin import SEMENT
import re
from pogg.semantic_composition.sement_util import POGGSEMENTUtil
from pogg.semantic_composition.call_tracer import SemCompTracer

class BooleanConstructionsMixin:
    """
    The `BooleanConstructionsMixin` contains functions for composing new SEMENTs where the version of one SEMENT is determined by a boolean value
    e.g. if an edge points to a boolean node, then depending on that value the SEMENT that should be generated from that edge will change
    """

    @SemCompTracer.trace
    def boolean_value(self, value: bool) -> SEMENT:
        # turning it into a SEMENT for consistency of what semantic composition functions return
        if value:
            return self.adjective("_true_a_of")
        else:
            return self.adjective("_false_a_of")

    @SemCompTracer.trace
    def boolean_edge(self, main_comp_fxn, boolean_value_node: SEMENT,
                     true_SEMENT: SEMENT, false_SEMENT: SEMENT, **kwargs):
        """eatenberry": {
            "comp_fxn": "boolean_edge",
            "main_comp_fxn": "prenominal_adjective",
            "boolean_value_node": "child",
            "true_SEMENT": {
                "comp_fxn": "adjective"
            },
            "false_SEMENT": {
                "comp_fxn": "adjective"
            },
            "adjective_SEMENT": "boolean_argument",
            "nominal_SEMENT": "parent"
        }"""
        pass

    @SemCompTracer.trace
    def boolean_property(self, boolean_node_SEMENT: SEMENT, modified_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
        key_rel = None
        for rel in boolean_node_SEMENT.rels:
            if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
                key_rel = rel
                break

        if key_rel:
            if key_rel.predicate == "_true_a_of":
                return self.generic_prenominal_descriptor(true_SEMENT, modified_SEMENT)
            else:
                return self.generic_prenominal_descriptor(false_SEMENT, modified_SEMENT)
        else:
            return None

    @SemCompTracer.trace
    def boolean_ARG1_relative_clause(self, boolean_node_SEMENT: SEMENT, ARG1_SEMENT: SEMENT, ARG2_SEMENT: SEMENT,
                                     true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
        key_rel = None
        for rel in boolean_node_SEMENT.rels:
            if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
                key_rel = rel
                break

        if key_rel:
            if key_rel.predicate == "_true_a_of":
                return self.ARG1_relative_clause(true_SEMENT, ARG1_SEMENT, ARG2_SEMENT)
            else:
                return self.ARG1_relative_clause(false_SEMENT, ARG1_SEMENT, ARG2_SEMENT)
        else:
            return None

    @SemCompTracer.trace
    def boolean_ARG2_relative_clause(self, boolean_node_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT,
                                     ARG2_SEMENT: SEMENT, ARG1_SEMENT: SEMENT=None) -> SEMENT:
        key_rel = None
        for rel in boolean_node_SEMENT.rels:
            if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
                key_rel = rel
                break

        if key_rel:
            if key_rel.predicate == "_true_a_of":
                return self.ARG2_relative_clause(true_SEMENT, ARG2_SEMENT)
            else:
                return self.ARG2_relative_clause(false_SEMENT, ARG2_SEMENT)
        else:
            return None