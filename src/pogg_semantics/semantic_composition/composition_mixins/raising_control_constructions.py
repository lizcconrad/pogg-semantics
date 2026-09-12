"""
The `raising_control_constructions` module contains the Mixin class for creating SEMENTs via raising and control constructions.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class RaisingAndControlConstructions:
    """
    The `RaisingAndControlConstructionsMixin` contains functions for creating SEMENTs via raising and control constructions.
    """

    # COMBINING PRED W/ PROPOSITION
    # using heuristics to guess the embedder slot just to simplify ...
    @SemCompTracer.trace
    def raising_predicate_and_proposition_seeking_proto_agent(self, raising_predicate_SEMENT: SEMENT, proposition_SEMENT: SEMENT) -> SEMENT:

        # "continue to sleep [empty ARG1]"

        SEMENTUtil.add_intrinsic_variable_property(raising_predicate_SEMENT, "TENSE", "tensed")

        # find h-type slot
        for slot_name, slot_value in raising_predicate_SEMENT.slots.items():
            if slot_value.startswith("h"):
                return self.semantic_algebra.op_raising(raising_predicate_SEMENT, proposition_SEMENT, slot_name, "ARG1")

    @SemCompTracer.trace
    def raising_predicate_and_proposition_seeking_proto_patient(self, raising_predicate_SEMENT: SEMENT, proposition_SEMENT: SEMENT) -> SEMENT:

        # "continue to be followed [empty ARG2] (by so-and-so, potentially filled already)"

        SEMENTUtil.add_intrinsic_variable_property(raising_predicate_SEMENT, "TENSE", "tensed")

        # find h-type slot
        for slot_name, slot_value in raising_predicate_SEMENT.slots.items():
            if slot_value.startswith("h"):
                return self.semantic_algebra.op_raising(raising_predicate_SEMENT, proposition_SEMENT, slot_name, "ARG2")



    @SemCompTracer.trace
    def raising_predicate_and_embedded_proto_agent(self, raising_predicate_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT) -> SEMENT:

        if not SEMENTUtil.check_if_quantified(proto_agent_SEMENT):
            quantified_agent = self.quantify_generic(proto_agent_SEMENT)
        else:
            quantified_agent = proto_agent_SEMENT

        return self.semantic_algebra.op_embedded_non_scopal_functor_hook_slots(raising_predicate_SEMENT,
                                                                               quantified_agent, "ARG1")

    @SemCompTracer.trace
    def raising_predicate_and_embedded_proto_patient(self, raising_predicate_SEMENT: SEMENT, proto_patient_SEMENT: SEMENT) -> SEMENT:

        if not SEMENTUtil.check_if_quantified(proto_patient_SEMENT):
            quantified_patient = self.quantify_generic(proto_patient_SEMENT)
        else:
            quantified_patient = proto_patient_SEMENT

        return self.semantic_algebra.op_embedded_non_scopal_functor_hook_slots(raising_predicate_SEMENT,
                                                                               quantified_patient, "ARG2")

    # COMBINING PRED W/ EMBEDDED ARG


    @SemCompTracer.trace
    def control_predicate_and_proposition_seeking_proto_agent(self, control_predicate_SEMENT: SEMENT, proposition_SEMENT: SEMENT) -> SEMENT:

        # "tried to run [empty ARG1]"

        SEMENTUtil.add_intrinsic_variable_property(control_predicate_SEMENT, "TENSE", "tensed")

        # find h-type slot
        embedder_slot = None
        controller_slot = None
        for slot_name, slot_value in control_predicate_SEMENT.slots.items():
            if slot_value.startswith("h"):
                embedder_slot = slot_name
            else:
                # if controller_slot hasn't been chosen OR the ARG# is higher than the already selected slot
                # e.g. ARG2 instead of ARG1
                # general heuristic that works in most cases where the more oblique argument is the controller
                # "I persuade *YOU* to sleep"
                # "promise" breaks the pattern
                if controller_slot is None or slot_name[-1] > controller_slot[-1]:
                    controller_slot = slot_name

        return self.semantic_algebra.op_control(control_predicate_SEMENT, proposition_SEMENT, embedder_slot, controller_slot, "ARG1")


    @SemCompTracer.trace
    def control_predicate_and_proposition_seeking_proto_patient(self, control_predicate_SEMENT: SEMENT, proposition_SEMENT: SEMENT) -> SEMENT:

        # "tried to be followed [empty ARG2]"

        # mark control_predicate as tensed
        SEMENTUtil.add_intrinsic_variable_property(control_predicate_SEMENT, "TENSE", "tensed")
        # mark proposition_predicate as untensed

        # find h-type slot
        embedder_slot = None
        controller_slot = None
        for slot_name, slot_value in control_predicate_SEMENT.slots.items():
            if slot_value.startswith("h"):
                embedder_slot = slot_name
            else:
                # if controller_slot hasn't been chosen OR the ARG# is higher than the already selected slot
                # e.g. ARG2 instead of ARG1
                # general heuristic that works in most cases where the more oblique argument is the controller
                # "I persuade *YOU* to sleep"
                # "promise" breaks the pattern
                if controller_slot is None or slot_name[-1] > controller_slot[-1]:
                    controller_slot = slot_name

        return self.semantic_algebra.op_control(control_predicate_SEMENT, proposition_SEMENT, embedder_slot,
                                                controller_slot, "ARG2")