from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil


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
    def boolean_edge(self, boolean_value_node: SEMENT,
                     true_SEMENT: SEMENT, false_SEMENT: SEMENT, main_comp_info):
        """eatenberry": {
            "comp_fxn": "boolean_edge",
            "boolean_value_node": "child",
            "true_SEMENT": {
                "comp_fxn": "adjective"
            },
            "false_SEMENT": {
                "comp_fxn": "adjective"
            },
            "main_comp_info": {
                "comp_fxn": "predicate_and_proto_agent",
                "predicate_SEMENT": "boolean_SEMENT",
                "proto_agent_SEMENT": "parent"
            },

        }"""
        # so this is the generic one
        boolean_key = SEMENTUtil.get_key_rel(boolean_value_node)
        if boolean_key.predicate == "_true_a_of":
            boolean_argument = true_SEMENT
        else:
            boolean_argument = false_SEMENT

        comp_fxn_obj = getattr(self, main_comp_info.composition_function_name)

        # TODO: maybe make a dict version? ... this is the only function that can't be used in isolation without the PIGGY package
        for param_name, param_val in main_comp_info.parameters.items():
            if param_val == "boolean_SEMENT":
                main_comp_info.parameters[param_name] = boolean_argument

        return comp_fxn_obj(**main_comp_info.parameters)





    @SemCompTracer.trace
    def boolean_property(self, boolean_node_SEMENT: SEMENT, modified_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
        key_rel = None
        for rel in boolean_node_SEMENT.rels:
            if boolean_node_SEMENT.index == rel.id and not (rel.predicate.endswith("_q") or rel.predicate.endswith("_q_i")):
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
            if boolean_node_SEMENT.index == rel.id and not (rel.predicate.endswith("_q") or rel.predicate.endswith("_q_i")):
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
            if boolean_node_SEMENT.index == rel.id and not (rel.predicate.endswith("_q") or rel.predicate.endswith("_q_i")):
                key_rel = rel
                break

        if key_rel:
            if key_rel.predicate == "_true_a_of":
                return self.ARG2_relative_clause(true_SEMENT, ARG2_SEMENT)
            else:
                return self.ARG2_relative_clause(false_SEMENT, ARG2_SEMENT)
        else:
            return None