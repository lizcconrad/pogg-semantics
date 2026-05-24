"""
The `base_constructions` module contains the Mixin class for creating SEMENTs from a number of "basic" constructions of English.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""

from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
from pogg.semantic_composition.sement_util import POGGSEMENTUtil

from pogg.semantic_composition.call_tracer import SemCompTracer

class BaseConstructionsMixin:
    """
    The `BaseConstructionsMixin` contains functions for composing new SEMENTs using two input SEMENTs.
    """
    # def noun_verbing_noun(self, verb_predicate: str, main_noun: SEMENT, modifying_noun: SEMENT) -> SEMENT:
    #     # create starter SEMENT of verb
    #     verb_SEMENT = self.verb(verb_predicate, {"PROG": "+"})
    #
    #     # check that modifying noun is quantified
    #     if not POGGSEMENTUtil.check_if_quantified(modifying_noun):
    #         quantified_modifying_noun = self.quantify_generic(modifying_noun)
    #     else:
    #         quantified_modifying_noun = modifying_noun
    #
    #     # plug arg2 with quantified_modifying_noun
    #     verb_arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook(verb_SEMENT, quantified_modifying_noun, "ARG2")
    #
    #     # plug result's arg1 with main_noun and use the main_noun as the hook
    #     # (we don't want this to be a "regular" sentence, we want the noun to be the semantic head)
    #     verb_arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook(verb_arg2_plugged, main_noun, "ARG1")
    #     return verb_arg1_plugged

    # def subject_verb_object(self, subject_SEMENT: SEMENT, verb_SEMENT: SEMENT, object_SEMENT: SEMENT):
    #     # `subject_SEMENT` is the SEMENT that would be realized as  the subject in active usage (e.g. 'the student' in 'the student bakes cookies')
    #     # `object_SEMENT is the SEMENT that would be realized as the object in active usage (e.g. 'cookies' in 'the student bakes cookies')
    #     object_and_verb = self.object_of_verb(verb_SEMENT, object_SEMENT)
    #     return self.semantic_algebra.op_non_scopal_functor_hook(object_and_verb, subject_SEMENT)

    @SemCompTracer.trace
    def ARG1_relative_clause(self,  verb_SEMENT: SEMENT, ARG1_SEMENT: SEMENT, ARG2_SEMENT: SEMENT=None):
        # :(
        # add TENSE: tensed to verb_SEMENT
        POGGSEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")

        if ARG2_SEMENT is None:
            verb_and_ARG2 = verb_SEMENT
        else:
            if not POGGSEMENTUtil.check_if_quantified(ARG2_SEMENT):
                quantified_ARG2 = self.quantify_generic(ARG2_SEMENT)
            else:
                quantified_ARG2 = ARG2_SEMENT
            verb_and_ARG2 = self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_ARG2, "ARG2")

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_and_ARG2, ARG1_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ARG2_relative_clause(self, verb_SEMENT: SEMENT, ARG2_SEMENT: SEMENT, ARG1_SEMENT: SEMENT=None):
        # :(
        # add TENSE: tensed to verb_SEMENT
        POGGSEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")

        if ARG1_SEMENT is None:
            verb_and_ARG1 = verb_SEMENT
        else:
            if not POGGSEMENTUtil.check_if_quantified(ARG1_SEMENT):
                quantified_ARG1 = self.quantify_generic(ARG1_SEMENT)
            else:
                quantified_ARG1 = ARG1_SEMENT
            verb_and_ARG1 = self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_ARG1, "ARG1")

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_and_ARG1, ARG2_SEMENT, "ARG2")

    @SemCompTracer.trace
    def prenominal_adjective(self, adjective_SEMENT: SEMENT, nominal_SEMENT: SEMENT) -> SEMENT:
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

        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adjective_SEMENT, nominal_SEMENT, "ARG1")

    @SemCompTracer.trace
    def nonrestrictive_adjectival_relative_clause(self, adjective_SEMENT: SEMENT, nominal_SEMENT: SEMENT):
        POGGSEMENTUtil.add_intrinsic_variable_property(adjective_SEMENT, "TENSE", "tensed")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(adjective_SEMENT, nominal_SEMENT, "ARG1")

    @SemCompTracer.trace
    def compound_noun(self, head_noun_SEMENT: SEMENT, non_head_noun_SEMENT: SEMENT) -> SEMENT:
        """
        Performs composition with two noun SEMENTs to get a compound noun SEMENT.
        e.g. "vanilla cake" or "computer desk"

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `head_noun_SEMENT` | `SEMENT` | SEMENT object for the head noun | *cake* in *vanilla cake* |
        | `non_head_noun_SEMENT` | `SEMENT` | SEMENT object for the non-head noun | *vanilla* in *vanilla cake* |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT composed of two nouns |
        """

        udef_q = self.quantifier("udef_q")
        # adding these variable properties avoids "the tailed light"
        # [ e SF: prop TENSE: untensed MOOD: indicative PROG: - PERF: - ]
        # minimally, just adding PROG: -
        compound = self.basic("compound", {"PROG": "-"})
        udef_non_head_noun = self.quantify(udef_q, non_head_noun_SEMENT)

        # plug ARG2 of compound (non_head)
        arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(compound, udef_non_head_noun, "ARG2")
        # plug ARG1 of compound (head)
        arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(arg2_plugged, head_noun_SEMENT, "ARG1")

        return arg1_plugged

    @SemCompTracer.trace
    def negation(self, negated_SEMENT: SEMENT) -> SEMENT:
        # introduce neg SEMENT

        neg_synopsis = {
            'roles': [
                {'name': 'ARG0',
                 'value': 'e'},
                {'name': 'ARG1',
                 'value': 'h'},
            ]
        }

        # add [ TENSE: tensed ] to negated_SEMENT
        POGGSEMENTUtil.add_intrinsic_variable_property(negated_SEMENT, "TENSE", "tensed")

        neg = self.semantic_algebra.create_base_SEMENT("neg", {'TENSE': 'tensed'}, neg_synopsis)
        return self.semantic_algebra.op_scopal_functor_index_argument_slots(neg, negated_SEMENT, "ARG1")

    @SemCompTracer.trace
    def object_of_noun(self, head_noun_SEMENT: SEMENT, object_noun_SEMENT: SEMENT):
        if not POGGSEMENTUtil.check_if_quantified(object_noun_SEMENT):
            if not POGGSEMENTUtil.check_if_quantified(object_noun_SEMENT):
                quantified_object = self.quantify_generic(object_noun_SEMENT)
            else:
                quantified_object = object_noun_SEMENT

            return self.semantic_algebra.op_non_scopal_functor_hook_slots(head_noun_SEMENT, quantified_object, "ARG1")

    @SemCompTracer.trace
    def object_of_verb(self, verb_SEMENT: SEMENT, object_SEMENT: SEMENT) -> SEMENT:
        # check if ground is quantified and quantify generically if not
        if not POGGSEMENTUtil.check_if_quantified(object_SEMENT):
            quantified_object = self.quantify_generic(object_SEMENT)
        else:
            quantified_object = object_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_object, "ARG2")

    @SemCompTracer.trace
    def cardinal_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # TODO: needs support for more than 1-9
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(number_SEMENT, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def ordinal_modifier(self, number_SEMENT: SEMENT, modified_SEMENT: SEMENT):
        # TODO: needs support for more than 1-9
        # get the CARG from the number_SEMENT and just make a new ordinal SEMENT
        for rel in number_SEMENT.rels:
            if rel.predicate == "card":
                digit = rel.carg

        ordinal_number = self.semantic_algebra.create_CARG_SEMENT("ord", digit)
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(ordinal_number, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def subject_of_verb(self, verb_SEMENT: SEMENT, subject_SEMENT: SEMENT) -> SEMENT:
        # check if ground is quantified and quantify generically if not
        if not POGGSEMENTUtil.check_if_quantified(subject_SEMENT):
            quantified_subject = self.quantify_generic(subject_SEMENT)
        else:
            quantified_subject = subject_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(verb_SEMENT, quantified_subject, "ARG1")

    @SemCompTracer.trace
    def passive_participle_modifier(self, participle_SEMENT: SEMENT, modified_SEMENT: SEMENT) -> SEMENT:
        # add variable property [PERF -] per https://delphinqa.ling.washington.edu/t/constraining-passive-participles/1156
        POGGSEMENTUtil.add_intrinsic_variable_property(participle_SEMENT, "PERF", "-")

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
        POGGSEMENTUtil.add_intrinsic_variable_property(participle_SEMENT, "PROG", "+")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(participle_SEMENT, modified_SEMENT, "ARG1")

    @SemCompTracer.trace
    def prepositional_relationship(self, preposition_predicate: str, figure_SEMENT: SEMENT, ground_SEMENT: SEMENT) -> SEMENT:
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

        preposition_SEMENT = self.preposition(preposition_predicate)

        # check if ground is quantified and quantify generically if not
        if not POGGSEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        # plug preposition's ARG2 with ground
        prep_arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(preposition_SEMENT, quantified_ground, "ARG2")
        # plug result of that's ARG1 with figure
        prep_arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(prep_arg2_plugged, figure_SEMENT, "ARG1")
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
    def relative_direction(self, direction_predicate: str, figure_SEMENT: SEMENT, ground_SEMENT: SEMENT) -> SEMENT:
        """
        1. introduce necessary SEMENTs
            - direction_SEMENT
            - loc_nonsp
            - place_n
        2. ensure ground_SEMENT is quantified
        3. plug ARG2 of direction_SEMENT with quantified_ground, result has functor as hook (appx. "...west of the school")
        4. plug ARG1 of (3) with place_n, result has argument hook (appx. "'place' west of the school")
        5. quantify (4) with `def_implicit_q`
        6. plug ARG2 of loc_nonsp with (5), result has functor hook
        7. plug ARG1 of loc_nonsp with figure_SEMENT, result has argument hook (appx. "house west of the school")
        """
        # 1. introduce necessary SEMENTs
        direction_SEMENT = self.adjective(direction_predicate)

        loc_nonsp_synopsis = {
            "roles": [
                {"name": "ARG0", "value": "e"},
                {"name": "ARG1", "value": "u"},
                {"name": "ARG2", "value": "x"}
            ]
        }
        loc_nonsp = self.manual_synopsis('loc_nonsp', loc_nonsp_synopsis)

        place_n = self.noun('place_n')

        # 2. ensure ground_SEMENT is quantified
        if not POGGSEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        # 3. plug ARG2 of direction_SEMENT with quantified_ground, result has functor as hook (result is "...west of the school")
        direction_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(direction_SEMENT, quantified_ground, "ARG2")

        # 4. plug ARG1 of (3) with place_n, result has argument hook (appx. "'place' west of the school")
        direction_ARG1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(direction_ARG2_plugged, place_n, "ARG1")

        # 5. quantify (4) with `def_implicit_q`
        def_imp = self.quantifier('def_implicit_q')
        quantified_direction_and_place = self.quantify(def_imp, direction_ARG1_plugged)

        # 6. plug ARG2 of loc_nonsp with (5), result has functor hook
        loc_nonsp_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(loc_nonsp, quantified_direction_and_place, "ARG2")

        # 7. plug ARG1 of loc_nonsp with figure_SEMENT, result has argument hook (appx. "house west of the school")
        loc_nonsp_ARG1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(loc_nonsp_ARG2_plugged, figure_SEMENT, "ARG1")
        return loc_nonsp_ARG1_plugged

    @SemCompTracer.trace
    def possessive(self, possessor_SEMENT: SEMENT, possessed_SEMENT: SEMENT) -> SEMENT:
        # check that possessor_SEMENT is quantified
        if not POGGSEMENTUtil.check_if_quantified(possessor_SEMENT):
            quantified_possessor = self.quantify_generic(possessor_SEMENT)
        else:
            quantified_possessor = possessor_SEMENT

        # introduce poss SEMENT
        poss_SEMENT = self.basic("poss")

        # plug ARG2 of poss with possessor
        poss_ARG1_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(poss_SEMENT, quantified_possessor, "ARG2")
        # plug ARG1 of poss with possessed and return
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(poss_ARG1_plugged, possessed_SEMENT, "ARG1")

    @SemCompTracer.trace
    def quantify(self, quantifier_SEMENT: SEMENT, quantified_SEMENT: SEMENT) -> SEMENT:
        return self.semantic_algebra.op_scopal_quantifier(quantifier_SEMENT, quantified_SEMENT)

    @SemCompTracer.trace
    def un_prefix(self, negated_SEMENT: SEMENT) -> SEMENT:
        """
        Creates a negated version of a SEMENT with the prefix "un", e.g. "unconscious".

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
        un_SEMENT = self.basic("_un-_a_neg")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(un_SEMENT, negated_SEMENT, "ARG1")

