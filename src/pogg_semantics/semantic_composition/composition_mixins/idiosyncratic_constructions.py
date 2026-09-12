"""
The `idiosyncratic_constructions` module contains the Mixin class for composing idiosyncratic SEMENTs that are more complex than typical plugging of arguments.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class IdiosyncraticConstructionsMixin:
    """
    The `IdiosyncraticConstructionsMixin` contains functions for composing idiosyncratic SEMENTs that are more complex than typical plugging of arguments.
    They often infolve introducing additional predicates that are specific to the construction and aren't obviously present from just the string alone but are required for correct semantics.
        - relative_direction -- "the house east of the lake" which requires introducing additional predicates (place_n, loc_nonsp)
        - measurement -- "the house is 20 feet tall" which requires introducing a "measure" predicate
    """


    @SemCompTracer.trace
    def measurement(self, measurement_adjective_SEMENT: SEMENT, measured_entity_SEMENT: SEMENT, measured_value_SEMENT: SEMENT) -> SEMENT:
        # introduce measure EP
        measure = self.basic("measure")

        # quantification checks
        if not SEMENTUtil.check_if_quantified(measured_entity_SEMENT):
            quant_measured = self.quantify_generic(measured_entity_SEMENT)
        else:
            quant_measured = measured_entity_SEMENT


        if not SEMENTUtil.check_if_quantified(measured_value_SEMENT):
            quant_value = self.quantify_generic(measured_value_SEMENT)
        else:
            quant_value = measured_value_SEMENT


        # add tense to adjective
        SEMENTUtil.add_intrinsic_variable_property(measurement_adjective_SEMENT, "TENSE", "tensed")


        # measurement_adjective.ARG1 = measured_entity.INDEX
        adj_and_ARG1 = self.semantic_algebra.op_non_scopal_functor_hook_slots(measurement_adjective_SEMENT, quant_measured, "ARG1")

        # plug measure.ARG2 with quant_value.INDEX
        measure_and_ARG2 = self.semantic_algebra.op_non_scopal_functor_hook_slots(measure, quant_value, "ARG2")
        # plug measure.ARG1 with adj_and_ARG1.INDEX
        # measure.ARG1 should be new INDEX
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(measure_and_ARG2, adj_and_ARG1, "ARG1")


    @SemCompTracer.trace
    def relative_direction(self, direction_SEMENT: SEMENT, figure_SEMENT: SEMENT, ground_SEMENT: SEMENT) -> SEMENT:
        """
        1. introduce necessary SEMENTs
            - loc_nonsp
            - place_n
        2. ensure ground_SEMENT is quantified
        3. plug ARG2 of direction_SEMENT with quantified_ground, result has functor as hook (appx. "...west of the school")
        4. plug ARG1 of (3) with place_n, result has argument hook (appx. "'place' west of the school")
        5. quantify (4) with `def_implicit_q`
        6. plug ARG2 of loc_nonsp with (5), result has functor hook
        7. plug ARG1 of loc_nonsp with figure_SEMENT, result has argument hook (appx. "house west of the school")
        """

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
        if not SEMENTUtil.check_if_quantified(ground_SEMENT):
            quantified_ground = self.quantify_generic(ground_SEMENT)
        else:
            quantified_ground = ground_SEMENT

        # 3. plug ARG2 of direction_SEMENT with quantified_ground, result has functor as hook (result is "...west of the school")
        direction_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(direction_SEMENT,
                                                                                        quantified_ground, "ARG2")

        # 4. plug ARG1 of (3) with place_n, result has argument hook (appx. "'place' west of the school")
        direction_ARG1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(direction_ARG2_plugged,
                                                                                         place_n, "ARG1")

        # 5. quantify (4) with `def_implicit_q`
        def_imp = self.quantifier('def_implicit_q')
        quantified_direction_and_place = self.quantify(def_imp, direction_ARG1_plugged)

        # 6. plug ARG2 of loc_nonsp with (5), result has functor hook
        loc_nonsp_ARG2_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(loc_nonsp,
                                                                                        quantified_direction_and_place,
                                                                                        "ARG2")

        # 7. plug ARG1 of loc_nonsp with figure_SEMENT, result has argument hook (appx. "house west of the school")
        loc_nonsp_ARG1_plugged = self.semantic_algebra.op_non_scopal_argument_hook_slots(loc_nonsp_ARG2_plugged,
                                                                                         figure_SEMENT, "ARG1")
        return loc_nonsp_ARG1_plugged