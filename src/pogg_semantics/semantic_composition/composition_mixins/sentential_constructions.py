"""
The `base_constructions` module contains the Mixin class for creating SEMENTs from a number of "basic" constructions of English.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class SententialConstructionsMixin:
    """
    The `SententialConstructionsMixin` contains functions for composing new SEMENTs using two input SEMENTs.
    """

    @SemCompTracer.trace
    def copula(self, subject_SEMENT: SEMENT, predicate_SEMENT: SEMENT, intrinsic_variable_properties: dict=None):
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        verb_SEMENT = self.verb("_be_v_id", intrinsic_variable_properties)
        SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "SF", "prop")
        SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")

        if not SEMENTUtil.check_if_quantified(subject_SEMENT):
            quantified_subject = self.quantify_generic(subject_SEMENT)
        else:
            quantified_subject = subject_SEMENT

        if not SEMENTUtil.check_if_quantified(predicate_SEMENT):
            quantified_object = self.quantify_generic(predicate_SEMENT)
        else:
            quantified_object = predicate_SEMENT

        verb_obj_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_object,
                                                                                  "ARG2")
        return self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_obj_plugged, quantified_subject, "ARG1")


    @SemCompTracer.trace
    def transitive_verb_sentence(self, verb_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT, proto_patient_SEMENT: SEMENT):
        if not SEMENTUtil.check_if_quantified(proto_agent_SEMENT):
            quantified_agent = self.quantify_generic(proto_agent_SEMENT)
        else:
            quantified_agent = proto_agent_SEMENT

        if not SEMENTUtil.check_if_quantified(proto_patient_SEMENT):
            quantified_patient = self.quantify_generic(proto_patient_SEMENT)
        else:
            quantified_patient = proto_patient_SEMENT

        verb_obj_plugged = self.predicate_and_proto_patient(verb_SEMENT, quantified_patient)
        return self.predicate_and_proto_agent(verb_obj_plugged, quantified_agent)



    @SemCompTracer.trace
    def intransitive_verb_sentence(self, verb_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT):
        if not SEMENTUtil.check_if_quantified(proto_agent_SEMENT):
            quantified_agent = self.quantify_generic(proto_agent_SEMENT)
        else:
            quantified_agent = proto_agent_SEMENT

        return self.predicate_and_proto_agent(verb_SEMENT, quantified_agent)

    @SemCompTracer.trace
    def intransitive_predicative_adjective_sentence(self, adjective_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT):
        if not SEMENTUtil.check_if_quantified(proto_agent_SEMENT):
            quantified_agent = self.quantify_generic(proto_agent_SEMENT)
        else:
            quantified_agent = proto_agent_SEMENT

        return self.predicate_and_proto_agent(adjective_SEMENT, quantified_agent)

    @SemCompTracer.trace
    def predicative_preposition_sentence(self, preposition_SEMENT: SEMENT, figure_SEMENT: SEMENT, ground_SEMENT: SEMENT):
        # check if ground is quantified and quantify generically if not
        if not SEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        if not SEMENTUtil.check_if_quantified(figure_SEMENT):
            quantified_figure = self.quantify_generic(figure_SEMENT)
        else:
            quantified_figure = figure_SEMENT

        # plug preposition's ARG2 with ground
        prep_arg2_plugged = self.predicate_and_proto_patient(preposition_SEMENT, quantified_ground)
        # plug result of that's ARG1 with figure
        prep_arg1_plugged = self.predicate_and_proto_agent(prep_arg2_plugged, quantified_figure)
        return prep_arg1_plugged