"""
The `predicative_constructions` module contains the Mixin class for creating SEMENTs using a predicate and its argument.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class PredicativeConstructionsMixin:
    """
    The `PredicativeConstructionsMixin` contains functions for composing new SEMENTs using a predicate and its argument.
    """

    @SemCompTracer.trace
    def predicate_and_proto_agent(self, predicative_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition with an adjective SEMENT and a nominal SEMENT
        e.g. "tasty cookie" or "tasty cookie in the oven"

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `adjective_SEMENT` | `SEMENT` | SEMENT object for the adjective | *tasty* in *tasty cookie in the oven* |
        | `nominal_SEMENT` | `SEMENT` | SEMENT object for the noun (plus potential adjuncts) that the adjective modifies | *cookie in the oven* in *tasty cookie in the oven* |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT composed of an adjective and the elements it modifies |
        """
        # CATEGORY: BASIC

        SEMENTUtil.add_intrinsic_variable_property(predicative_SEMENT, "TENSE", "tensed")

        if not SEMENTUtil.check_if_quantified(proto_agent_SEMENT):
            quantified_agent = self.quantify_generic(proto_agent_SEMENT)
        else:
            quantified_agent = proto_agent_SEMENT

        # # determine scopal or non-scopal based on slot's variable type
        # if predicative_SEMENT.slots["ARG1"].startswith("h"):
        #     return self.semantic_algebra.op_scopal_functor_index_slots(predicative_SEMENT, quantified_agent, "ARG1")
        # else:
        return self.semantic_algebra.op_non_scopal_functor_hook_slots(predicative_SEMENT, quantified_agent, "ARG1")

    @SemCompTracer.trace
    def predicate_and_proto_patient(self, predicative_SEMENT: SEMENT, proto_patient_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition with an adjective SEMENT and a nominal SEMENT
        e.g. "tasty cookie" or "tasty cookie in the oven"

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `adjective_SEMENT` | `SEMENT` | SEMENT object for the adjective | *tasty* in *tasty cookie in the oven* |
        | `nominal_SEMENT` | `SEMENT` | SEMENT object for the noun (plus potential adjuncts) that the adjective modifies | *cookie in the oven* in *tasty cookie in the oven* |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT composed of an adjective and the elements it modifies |
        """
        # CATEGORY: BASIC

        SEMENTUtil.add_intrinsic_variable_property(predicative_SEMENT, "TENSE", "tensed")

        if not SEMENTUtil.check_if_quantified(proto_patient_SEMENT):
            quantified_patient = self.quantify_generic(proto_patient_SEMENT)
        else:
            quantified_patient = proto_patient_SEMENT

        # # determine scopal or non-scopal based on slot's variable type
        # if predicative_SEMENT.slots["ARG2"].startswith("h"):
        #     return self.semantic_algebra.op_scopal_functor_index_slots(predicative_SEMENT, quantified_patient, "ARG2")
        # else:
        return self.semantic_algebra.op_non_scopal_functor_hook_slots(predicative_SEMENT, quantified_patient, "ARG2")

    @SemCompTracer.trace
    def predicate_and_oblique(self, predicative_SEMENT: SEMENT, oblique_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition with an adjective SEMENT and a nominal SEMENT
        e.g. "tasty cookie" or "tasty cookie in the oven"

        **Parameters**`
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `adjective_SEMENT` | `SEMENT` | SEMENT object for the adjective | *tasty* in *tasty cookie in the oven* |
        | `nominal_SEMENT` | `SEMENT` | SEMENT object for the noun (plus potential adjuncts) that the adjective modifies | *cookie in the oven* in *tasty cookie in the oven* |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT composed of an adjective and the elements it modifies |
        """
        # CATEGORY: BASIC

        SEMENTUtil.add_intrinsic_variable_property(predicative_SEMENT, "TENSE", "tensed")

        if not SEMENTUtil.check_if_quantified(oblique_SEMENT):
            quantified_oblique = self.quantify_generic(oblique_SEMENT)
        else:
            quantified_oblique = oblique_SEMENT

        # determine scopal or non-scopal based on slot's variable type
        # if predicative_SEMENT.slots["ARG3"].startswith("h"):
        #     return self.semantic_algebra.op_scopal_functor_index_slots(predicative_SEMENT, quantified_oblique, "ARG3")
        # else:
        return self.semantic_algebra.op_non_scopal_functor_hook_slots(predicative_SEMENT, quantified_oblique, "ARG3")

    @SemCompTracer.trace
    def preposition_and_ground(self, preposition_SEMENT: SEMENT, ground_SEMENT: SEMENT):
        if not SEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(preposition_SEMENT, quantified_ground, "ARG2")


    @SemCompTracer.trace
    def subordinating_conjunction_and_figure(self, conjunction_SEMENT: SEMENT, figure_SEMENT: SEMENT) -> SEMENT:

        # figure proposition must be tensed
        SEMENTUtil.add_intrinsic_variable_property(figure_SEMENT, "TENSE", "tensed")

        return self.semantic_algebra.op_scopal_functor_index_slots(conjunction_SEMENT, figure_SEMENT, "ARG1")

    @SemCompTracer.trace
    def subordinating_conjunction_and_ground(self, conjunction_SEMENT: SEMENT, ground_SEMENT: SEMENT) -> SEMENT:

        # ground proposition must be tensed
        SEMENTUtil.add_intrinsic_variable_property(ground_SEMENT, "TENSE", "tensed")

        return self.semantic_algebra.op_scopal_functor_index_slots(conjunction_SEMENT, ground_SEMENT, "ARG2")