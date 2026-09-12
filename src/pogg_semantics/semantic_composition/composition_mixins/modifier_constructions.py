"""
The `modifier_constructions` module contains the Mixin class for creating SEMENTs with a modifier and a SEMENT that it modifiers.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class ModifierConstructionsMixin:
    """
    The `ModifierConstructionsMixin` contains functions for composing new SEMENTs a modifier SEMENT and a SEMENT being modified.
    """

    @SemCompTracer.trace
    def adjective_as_modifier(self, adjectival_modifier_SEMENT: SEMENT, nominal_modified_SEMENT: SEMENT) -> SEMENT:
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

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adjectival_modifier_SEMENT, nominal_modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def adverb_as_modifier(self, adverbial_modifier_SEMENT: SEMENT, verbal_modified_SEMENT: SEMENT) -> SEMENT:
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

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adverbial_modifier_SEMENT,
                                                                       verbal_modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def cardinal_num_as_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # NOTE: changed the name here!!!
        # CATEGORY: BASIC
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(number_SEMENT, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ordinal_num_as_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # CATEGORY: BASIC
        # get the CARG from the number_SEMENT and just make a new ordinal SEMENT
        for rel in number_SEMENT.rels:
            if rel.predicate == "card":
                digit = rel.carg

        ordinal_number = self.semantic_algebra.create_CARG_SEMENT("ord", digit)
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(ordinal_number, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def prepositional_phrase_as_modifier(self, prepositional_modifier_SEMENT: SEMENT, modified_SEMENT: SEMENT) -> SEMENT:
        # CATEGORY: BASIC
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(prepositional_modifier_SEMENT, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def relative_predicate_and_proto_agent(self, relative_predicate_SEMENT: SEMENT,
                                           proto_agent_SEMENT: SEMENT) -> SEMENT:
        # todo: better handling???
        # if tense or prog not specified, just do TENSE: tensed
        if "TENSE" not in relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]:
            relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]["TENSE"] = "tensed"

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(relative_predicate_SEMENT, proto_agent_SEMENT,
                                                                       "ARG1")

    @SemCompTracer.trace
    def relative_predicate_and_proto_patient(self, relative_predicate_SEMENT: SEMENT,
                                             proto_patient_SEMENT: SEMENT) -> SEMENT:

        if "TENSE" not in relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]:
            relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]["TENSE"] = "tensed"

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(relative_predicate_SEMENT, proto_patient_SEMENT,
                                                                       "ARG2")

    @SemCompTracer.trace
    def relative_predicate_and_oblique(self, relative_predicate_SEMENT: SEMENT, oblique_SEMENT: SEMENT) -> SEMENT:
        # todo: better handling???
        # if tense or prog not specified, just do TENSE: tensed
        if "TENSE" not in relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]:
            relative_predicate_SEMENT.variables[relative_predicate_SEMENT.index]["TENSE"] = "tensed"

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(relative_predicate_SEMENT, oblique_SEMENT,
                                                                       "ARG3")

    @SemCompTracer.trace
    def modifying_participle_and_proto_agent(self, participle_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT) -> SEMENT:

        # remove TENSE if it's already on the participle_SEMENT ...
        # TODO: this is unusual but idk ...
        if "TENSE" in participle_SEMENT.variables[participle_SEMENT.index]:
            participle_SEMENT.variables[participle_SEMENT.index].pop("TENSE")

        if "PROG" not in participle_SEMENT.variables[participle_SEMENT.index]:
            participle_SEMENT.variables[participle_SEMENT.index]["PROG"] = "+"

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, proto_agent_SEMENT, "ARG1")

    @SemCompTracer.trace
    def modifying_participle_and_proto_patient(self, participle_SEMENT: SEMENT, proto_patient_SEMENT: SEMENT) -> SEMENT:

        # remove TENSE if it's already on the participle_SEMENT ...
        # TODO: this is unusual but idk ...
        if "TENSE" in participle_SEMENT.variables[participle_SEMENT.index]:
            participle_SEMENT.variables[participle_SEMENT.index].pop("TENSE")

        modified_sement = self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, proto_patient_SEMENT, "ARG2")

        # add icons topic relation between verb's ARG0 and ARG2
        # get the ARG2 variable from the participle_SEMENT's slots (???)
        topic_icons = mrs.ICons(participle_SEMENT.index, "topic", participle_SEMENT.slots["ARG2"])
        modified_sement.icons.append(topic_icons)

        return modified_sement


    # TODO: do i need this one ... ?
    @SemCompTracer.trace
    def modifying_participle_and_oblique(self, participle_SEMENT: SEMENT, oblique_SEMENT: SEMENT) -> SEMENT:

        # remove TENSE if it's already on the participle_SEMENT ...
        # TODO: this is unusual but idk ...
        if "TENSE" in participle_SEMENT.variables[participle_SEMENT.index]:
            participle_SEMENT.variables[participle_SEMENT.index].pop("TENSE")

        modified_sement = self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, oblique_SEMENT, "ARG3")

        # add icons topic relation between verb's ARG0 and ARG2
        # get the ARG2 variable from the participle_SEMENT's slots (???)
        topic_icons = mrs.ICons(participle_SEMENT.index, "topic", participle_SEMENT.slots["ARG3"])
        modified_sement.icons.append(topic_icons)

        return modified_sement

    # TODO: not sure I need this? but it definitely needs a better name
    @SemCompTracer.trace
    def verbal_modifier(self, modifier_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # modifier is the functor
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(modifier_SEMENT, modified_SEMENT, "ARG1")




