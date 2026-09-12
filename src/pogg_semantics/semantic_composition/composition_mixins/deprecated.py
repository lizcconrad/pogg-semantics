"""
The `deprecated` module contains the Mixin class for with functions for creating SEMENTs that have been deprecated in newer versions.
"""
import re
from delphin import mrs
from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer


class DeprecatedMixin:
    """
    The `DeprecatedMixin` class contains functions for creating SEMENTs that have been deprecated in newer versions.
    """

    @SemCompTracer.trace
    def proper_noun(self, name: str, intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        Creates a SEMENT for a named entity, e.g. a person ("Liz").

        DEPRECATION REASON: doesn't correctly handle quantification, also a "proper noun" doesn't have to just be a name, so it's a misnomer

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `name` | `str` | | | `'Liz'` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'PERS': '3'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT("named", name, intrinsic_variable_properties)

    @SemCompTracer.trace
    def prenominal_adjective(self, adjective_SEMENT: SEMENT, nominal_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition with an adjective SEMENT and a nominal SEMENT
        e.g. "tasty cookie" or "tasty cookie in the oven"

        DEPRECATON REASON: misnomer, "prenominal adjective" is syntax speak, the semantics are the same for "nut free," so renamed this

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

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adjective_SEMENT, nominal_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ARG1_relative_clause(self, verb_SEMENT: SEMENT, ARG1_SEMENT: SEMENT, ARG2_SEMENT: SEMENT = None):
        # changed to subject_clausal_modifier ... ugh

        # add TENSE: tensed to verb_SEMENT
        SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")

        if ARG2_SEMENT is None:
            verb_and_ARG2 = verb_SEMENT
        else:
            if not SEMENTUtil.check_if_quantified(ARG2_SEMENT):
                quantified_ARG2 = self.quantify_generic(ARG2_SEMENT)
            else:
                quantified_ARG2 = ARG2_SEMENT
            verb_and_ARG2 = self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_ARG2, "ARG2")

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_and_ARG2, ARG1_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ARG2_relative_clause(self, verb_SEMENT: SEMENT, ARG2_SEMENT: SEMENT, ARG1_SEMENT: SEMENT = None):
        # changed to objet_clausal_modifier ... ugh


        # add TENSE: tensed to verb_SEMENT
        SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")

        if ARG1_SEMENT is None:
            verb_and_ARG1 = verb_SEMENT
        else:
            if not SEMENTUtil.check_if_quantified(ARG1_SEMENT):
                quantified_ARG1 = self.quantify_generic(ARG1_SEMENT)
            else:
                quantified_ARG1 = ARG1_SEMENT
            verb_and_ARG1 = self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_ARG1, "ARG1")

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_and_ARG1, ARG2_SEMENT, "ARG2")

    @SemCompTracer.trace
    def nonrestrictive_adjectival_relative_clause(self, adjective_SEMENT: SEMENT, nominal_SEMENT: SEMENT):
        SEMENTUtil.add_intrinsic_variable_property(adjective_SEMENT, "TENSE", "tensed")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adjective_SEMENT, nominal_SEMENT, "ARG1")

    # TODO: wrong place ... ?
    @SemCompTracer.trace
    def object_of_verb(self, verb_SEMENT: SEMENT, object_SEMENT: SEMENT) -> SEMENT:
        # check if ground is quantified and quantify generically if not
        if not SEMENTUtil.check_if_quantified(object_SEMENT):
            quantified_object = self.quantify_generic(object_SEMENT)
        else:
            quantified_object = object_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_object, "ARG2")

    @SemCompTracer.trace
    def cardinal_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(number_SEMENT, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ordinal_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # get the CARG from the number_SEMENT and just make a new ordinal SEMENT
        for rel in number_SEMENT.rels:
            if rel.predicate == "card":
                digit = rel.carg

        ordinal_number = self.semantic_algebra.create_CARG_SEMENT("ord", digit)
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(ordinal_number, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def prepositional_relationship(self, preposition_SEMENT: SEMENT, figure_SEMENT: SEMENT,
                                   ground_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition between two SEMENTs and an introduced prepositional predicate
        to get a SEMENT representing a prepositional relationship.
        e.g. "book inside the box" or "bench at the park"

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `prepositional_predicate` | `str` | ERG predicate label for the preposition | `_in_p_loc` |
        | `figure_SEMENT` | `SEMENT` | SEMENT object for the figure in the relationship | *book* in *book inside the box* |
        | `ground_SEMENT` | `SEMENT` | SEMENT object for the ground in the relationship | *box* in *book inside the box* |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT representing the prepositional relationship |
        """

        # check if ground is quantified and quantify generically if not
        if not SEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        # plug preposition's ARG2 with ground
        prep_arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(preposition_SEMENT,
                                                                                   quantified_ground, "ARG2")
        # plug result of that's ARG1 with figure
        prep_arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(prep_arg2_plugged, figure_SEMENT,
                                                                                    "ARG1")
        return prep_arg1_plugged

    # def subject_relative_clause(self, relative_clause_SEMENT: SEMENT, nominal_SEMENT: SEMENT) -> SEMENT:
    #     # set the relative clause's INDEX variable to have TENSE: tensed and PERF: bool
    #     # this lets us get the "...who Xd" in various tenses
    #     if "TENSE" not in relative_clause_SEMENT.variables[relative_clause_SEMENT.index]:
    #         relative_clause_SEMENT.variables[relative_clause_SEMENT.index]["TENSE"] = "tensed"
    #     if "TENSE" not in relative_clause_SEMENT.variables[relative_clause_SEMENT.index]:
    #         relative_clause_SEMENT.variables[relative_clause_SEMENT.index]["PERF"] = "bool"
    #     # subject relative clause
    #     # the person who baked a cookie
    #     # below are others that i may or may not need to account for ...
    #     # vs. "the cookie that the person baked" ...
    #     # vs. "the person who Liz told to bake the cookie"
    #     # "the person that Liz said baked the cookie"
    #     # "the person whose recipe was used to bake cookies" :(
    #     return self.semantic_algebra.op_non_scopal_argument_hook(relative_clause_SEMENT, nominal_SEMENT, "ARG1")
    #
    # def object_relative_clause(self, relative_clause_SEMENT: SEMENT, nominal_SEMENT: SEMENT) -> SEMENT:
    #     # set the relative clause's INDEX variable to have TENSE: tensed and PERF: bool
    #     # this lets us get the "...who Xd" in various tenses
    #     if "TENSE" not in relative_clause_SEMENT.variables[relative_clause_SEMENT.index]:
    #         relative_clause_SEMENT.variables[relative_clause_SEMENT.index]["TENSE"] = "tensed"
    #     if "TENSE" not in relative_clause_SEMENT.variables[relative_clause_SEMENT.index]:
    #         relative_clause_SEMENT.variables[relative_clause_SEMENT.index]["PERF"] = "bool"
    #     # "the cookie that the person baked" ...
    #     # vs. "the person who Liz told to bake the cookie"
    #     # "the person that Liz said baked the cookie"
    #     # "the person whose recipe was used to bake cookies" :(
    #     return self.semantic_algebra.op_non_scopal_argument_hook(relative_clause_SEMENT, nominal_SEMENT, "ARG2")

    @SemCompTracer.trace
    def subject_of_verb(self, verb_SEMENT: SEMENT, subject_SEMENT: SEMENT) -> SEMENT:
        # check if ground is quantified and quantify generically if not
        if not SEMENTUtil.check_if_quantified(subject_SEMENT):
            quantified_subject = self.quantify_generic(subject_SEMENT)
        else:
            quantified_subject = subject_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_subject, "ARG1")


    @SemCompTracer.trace
    def generic_prenominal_descriptor(self, descriptor_SEMENT: SEMENT, described_SEMENT: SEMENT) -> SEMENT:
        # edges labeled "descriptor" may have an adjective or a participle as their child
        # so the function has to determine which type of descriptor it has and do composition based on that

        descriptor_key_rel = SEMENTUtil.get_key_rel(descriptor_SEMENT)

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
            described_key_rel = SEMENTUtil.get_key_rel(described_SEMENT)
            if described_key_rel.predicate == 'named':
                return self.nonrestrictive_adjectival_relative_clause(descriptor_SEMENT, described_SEMENT)
            else:
                return self.prenominal_adjective(descriptor_SEMENT, described_SEMENT)

    @SemCompTracer.trace
    def passive_participle_modifier(self, participle_SEMENT: SEMENT, modified_SEMENT: SEMENT) -> SEMENT:
        # add variable property [PERF -] per https://delphinqa.ling.washington.edu/t/constraining-passive-participles/1156
        SEMENTUtil.add_intrinsic_variable_property(participle_SEMENT, "PERF", "-")

        # e.g. "broken window"
        passive_SEMENT = self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, modified_SEMENT, "ARG2")

        # add icons topic relation between verb's ARG0 and ARG2
        # get the ARG2 variable from the participle_SEMENT's slots (???)
        topic_icons = mrs.ICons(participle_SEMENT.index, "topic", participle_SEMENT.slots["ARG2"])
        passive_SEMENT.icons.append(topic_icons)

        return passive_SEMENT

    @SemCompTracer.trace
    def present_participle_modifier(self, participle_SEMENT: SEMENT, modified_SEMENT: SEMENT) -> SEMENT:
        # e.g. "glowing flower"
        # make sure index of participle_SEMENT has PROG: +
        SEMENTUtil.add_intrinsic_variable_property(participle_SEMENT, "PROG", "+")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, modified_SEMENT, "ARG1")
