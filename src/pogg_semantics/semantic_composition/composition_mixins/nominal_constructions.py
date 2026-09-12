"""
The `nominal_constructions` module contains the Mixin class for creating SEMENTs where the result is roughly "nouny"

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy
from typing import override

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT, sementcodecs
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class NominalConstructionsMixin:
    """
    The `NominalConstructionsMixin` contains functions for composing new SEMENTs where the result is roughly "nouny"
    """

    @SemCompTracer.trace
    def appositive(self, first_nominal_SEMENT: SEMENT, second_nominal_SEMENT: SEMENT):
        appos = self.basic("appos")

        # check each nominal for quantification and quantify if it's not
        # BOTH members should be quantified before plugging appos slots
        if not SEMENTUtil.check_if_quantified(first_nominal_SEMENT):
            quantified_first = self.quantify_generic(first_nominal_SEMENT)
        else:
            quantified_first = first_nominal_SEMENT

        if not SEMENTUtil.check_if_quantified(second_nominal_SEMENT):
            quantified_second = self.quantify_generic(second_nominal_SEMENT)
        else:
            quantified_second = second_nominal_SEMENT

        # plug appos.ARG2 with second_nominal
        appos_arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(appos, quantified_second, "ARG2")
        # plug result of that's ARG1 with first_nominal
        appos_arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(appos_arg2_plugged, quantified_first, "ARG1")

        return appos_arg1_plugged

    @SemCompTracer.trace
    def date(self, day: str=None, month: str=None, year: str=None, intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        """
        months = {
            "1": "Jan",
            "2": "Feb",
            "3": "Mar",
            "4": "Apr",
            "5": "May",
            "6": "Jun",
            "7": "Jul",
            "8": "Aug",
            "9": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        if month != "":
            month = months[month]

        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        # just put in what's entered for day, month, and year
        # it'll generate or it won't

        # TODO: should i be doing this ...?
        if day in ["11", "12", "13", "14", "15", "16", "17", "18", "19"]:
            day = day + "th"
        elif day.endswith("1"):
            day = day + "st"
        elif day.endswith("2"):
            day = day + "nd"
        elif day.endswith("3"):
            day = day + "rd"
        elif day != "":
            day = day + "th"

        day_SEMENT = self.semantic_algebra.create_CARG_SEMENT("dofm", day)
        month_SEMENT = self.semantic_algebra.create_CARG_SEMENT("mofy", month, {"NUM": "sg"})
        year_SEMENT = self.semantic_algebra.create_CARG_SEMENT("yofc", year)

        # all three
        if day != "" and month != "" and year != "":
            year_q = self.quantifier("proper_q")
            quantified_year = self.quantify(year_q, year_SEMENT)
            # plug ARG1 of dofm with year for some reason ... ?
            dofm_ARG1_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(day_SEMENT, quantified_year, "ARG1")
            # introduce "of" and quantify month
            of_p = self.basic("of_p")
            month_q = self.quantifier("def_implicit_q")
            quantified_month = self.quantify(month_q, month_SEMENT)
            # plug ARG2 of "of" with mofy
            of_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(of_p, quantified_month, "ARG2")
            # plug ARG1 of "of" with dofm
            date_SEMENT = self.semantic_algebra.op_non_scopal_argument_hook_slots(of_ARG2_plugged, dofm_ARG1_plugged, "ARG1")
        # month year
        elif month != "" and year != "":
            year_q = self.quantifier("proper_q")
            quantified_year = self.quantify(year_q, year_SEMENT)
            # plug ARG1 of "mofy" with the year
            mofy_ARG1_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(month_SEMENT, quantified_year, "ARG1")
            # force proper_q on month
            month_q = self.quantifier("proper_q")
            date_SEMENT = self.quantify(month_q, mofy_ARG1_plugged)
        # day month
        elif day != "" and month != "":
            of_p = self.basic("of_p")
            # use implicit quantifier for month
            month_q = self.quantifier("def_implicit_q")
            quantified_month = self.quantify(month_q, month_SEMENT)
            # plug ARG2 of "of" with the month
            of_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(of_p, quantified_month, "ARG2")
            # plug ARG1 of "of" with day (unquantified)
            date_SEMENT = self.semantic_algebra.op_non_scopal_argument_hook_slots(of_ARG2_plugged, day_SEMENT, "ARG1")

        # just year
        elif year != "":
            year_q = self.quantifier("proper_q")
            date_SEMENT = self.quantify(year_q, year_SEMENT)
        # just month
        elif month != "":
            month_q = self.quantifier("proper_q")
            date_SEMENT = self.quantify(month_q, month_SEMENT)
        # just day
        elif day != "":
            # forcing "the" when it's just the day ?
            # mmm but sometimes you want to say "every 15th of the month" ... so maybe not
            day_q = self.quantifier("_the_q")
            date_SEMENT = self.quantify(day_q, day_SEMENT)
        else:
            return None

        return date_SEMENT

    @SemCompTracer.trace
    def compound_location(self, head_noun_SEMENT: SEMENT, non_head_noun_SEMENT: SEMENT) -> SEMENT:
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
        # TODO: would prefer for loc_compound to be in SEMI...
        compound = self.manual_synopsis("loc_compound", {
            "roles": [
                {"name": "ARG0", "value": "e"},
                {"name": "ARG1", "value": "u"},
                {"name": "ARG2", "value": "u"}
            ]
        })
        # compound = self.basic("compound")
        quantify_non_head_noun = self.quantify_generic(non_head_noun_SEMENT)

        # plug ARG2 of compound (non_head)
        arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(compound, quantify_non_head_noun, "ARG2")
        # plug ARG1 of compound (head)
        arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(arg2_plugged, head_noun_SEMENT, "ARG1")

        return arg1_plugged

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
        # CATEGORY: BASIC (?)

        # plug ARG2 of compound (non_head)
        # TODO: here ? or post processing ?
        # if "NUM" not in non_head_noun_SEMENT.variables[non_head_noun_SEMENT.index]:
        #     non_head_noun_SEMENT.variables[non_head_noun_SEMENT.index]["NUM"] = "sg"

        # only do this if the *HEAD* is NOT pl
        SEMENTUtil.add_intrinsic_variable_property(non_head_noun_SEMENT, "NUM", "sg")


        # adding these variable properties avoids "the tailed light"
        # [ e SF: prop TENSE: untensed MOOD: indicative PROG: - PERF: - ]
        # minimally, just adding PROG: -
        compound = self.basic("compound")
        # use existential_q for non_head
        if not SEMENTUtil.check_if_quantified(non_head_noun_SEMENT):
            udef_q = self.quantifier("existential_q")
            quantify_non_head_noun = self.quantify(udef_q, non_head_noun_SEMENT)
        else:
            quantify_non_head_noun = non_head_noun_SEMENT

        arg2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(compound, quantify_non_head_noun, "ARG2")
        # plug ARG1 of compound (head)
        arg1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(arg2_plugged, head_noun_SEMENT, "ARG1")

        return arg1_plugged

    @SemCompTracer.trace
    def noun_and_complement(self, head_noun_SEMENT: SEMENT, complement_noun_SEMENT: SEMENT):
        # CATEGORY: BASIC

        if not SEMENTUtil.check_if_quantified(complement_noun_SEMENT):
            quantified_complement = self.quantify_generic(complement_noun_SEMENT)
        else:
            quantified_complement = complement_noun_SEMENT

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(head_noun_SEMENT, quantified_complement, "ARG1")

    @SemCompTracer.trace
    def number_with_unit(self, number_SEMENT: SEMENT, unit_SEMENT: SEMENT):
        # CATEGORY: BASIC (?)
        # TODO: hacky...
        # if the unit comes with an ad-hoc quantifier (e.g. proper_q), remove it for this scenario
        SEMENTUtil.add_intrinsic_variable_property(unit_SEMENT, "QUANT", "udef_q", override=True)

        # instead of popping change it to udef_q for later

        num_with_unit = self.semantic_algebra.op_non_scopal_argument_hook_slots(number_SEMENT, unit_SEMENT, "ARG1")

        return num_with_unit

    @SemCompTracer.trace
    def possessive(self, possessor_SEMENT: SEMENT, possessed_SEMENT: SEMENT) -> SEMENT:
        # CATEGORY: BASic

        # check that possessor_SEMENT is quantified
        if not SEMENTUtil.check_if_quantified(possessor_SEMENT):
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
        # CATEGORY: BASIC

        # if the quantified_SEMENT's INDEX has an ad-hoc QUANT feature, pop it
        if 'QUANT' in quantified_SEMENT.variables[quantified_SEMENT.index]:
            # remove ad-hoc QUANT feature
            quantified_SEMENT.variables[quantified_SEMENT.index].pop('QUANT')
        return self.semantic_algebra.op_scopal_quantifier(quantifier_SEMENT, quantified_SEMENT)


    @SemCompTracer.trace
    def figure_preposition_ground(self, preposition_SEMENT: SEMENT, figure_SEMENT: SEMENT, ground_SEMENT: SEMENT) -> SEMENT:
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

    # @SemCompTracer.trace
    # def proto_agent_relative_clause(self, verb_SEMENT: SEMENT, proto_agent_SEMENT: SEMENT):
    #     # add TENSE: tensed to verb_SEMENT
    #     SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")
    #
    #     return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_SEMENT, proto_agent_SEMENT, "ARG1")
    #
    # @SemCompTracer.trace
    # def proto_patient_relative_clause(self, verb_SEMENT: SEMENT, proto_patient_SEMENT: SEMENT):
    #     # add TENSE: tensed to verb_SEMENT
    #     SEMENTUtil.add_intrinsic_variable_property(verb_SEMENT, "TENSE", "tensed")
    #
    #     return self.semantic_algebra.op_non_scopal_argument_hook_slots(verb_SEMENT, proto_patient_SEMENT, "ARG2")
    #


