"""
The `misc_constructions` module contains the Mixin class for composing SEMENTs using constructions that don't fit into any other category.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class MiscConstructionsMixin:
    """
    The `MiscConstructionsMixin` contains functions for composing SEMENTs using constructions that don't fit into any other category.
    """

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
        SEMENTUtil.add_intrinsic_variable_property(negated_SEMENT, "TENSE", "tensed")

        neg = self.semantic_algebra.create_base_SEMENT("neg", {'TENSE': 'tensed'}, neg_synopsis)
        return self.semantic_algebra.op_scopal_functor_index_argument_slots(neg, negated_SEMENT, "ARG1")

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