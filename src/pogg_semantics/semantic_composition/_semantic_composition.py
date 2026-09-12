"""
The base_constructions module contains classes that help in creating SEMENTs from scratch as well as performing composition on existing SEMENTs.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""

from pathlib import Path
from pogg_semantics.pogg_config import POGGCompositionConfig

from pogg_semantics.semantic_composition._semantic_algebra import SemanticAlgebra
from pogg_semantics.semantic_composition.composition_mixins.single_word_constructions import SingleWordConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.nominal_constructions import NominalConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.modifier_constructions import ModifierConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.predicative_constructions import PredicativeConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.raising_control_constructions import RaisingAndControlConstructions
from pogg_semantics.semantic_composition.composition_mixins.coordination_constructions import CoordinationConstructionsMixin

# slightly unusual
from pogg_semantics.semantic_composition.composition_mixins.idiosyncratic_constructions import IdiosyncraticConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.misc_constructions import MiscConstructionsMixin

# bodies of these functions call functions from other categories
from pogg_semantics.semantic_composition.composition_mixins.sentential_constructions import SententialConstructionsMixin
from pogg_semantics.semantic_composition.composition_mixins.heuristic_constructions import HeuristicConstructionsMixin

# super specific to one dataset... not sure if i should keep
from pogg_semantics.semantic_composition.composition_mixins.boolean_constructions import BooleanConstructionsMixin

# not in use for now but possibly later
from pogg_semantics.semantic_composition.composition_mixins.surgical_constructions import SurgicalConstructionsMixin

# uncategorized
from pogg_semantics.semantic_composition.composition_mixins.temporary_constructions import TemporaryConstructionsMixin

# accomodating older datasets with older versions
from pogg_semantics.semantic_composition.composition_mixins.deprecated import DeprecatedMixin
# TODO: how can i make these optional?

class SemanticComposition(SingleWordConstructionsMixin,
                            NominalConstructionsMixin,
                            ModifierConstructionsMixin,
                            PredicativeConstructionsMixin,
                            RaisingAndControlConstructions,
                            CoordinationConstructionsMixin,
                            IdiosyncraticConstructionsMixin,
                            MiscConstructionsMixin,
                            SententialConstructionsMixin,
                            HeuristicConstructionsMixin,
                            BooleanConstructionsMixin,
                            SurgicalConstructionsMixin,
                            TemporaryConstructionsMixin,
                            DeprecatedMixin):
    """
    The SemanticComposition class inherits from the various "mixin" classes that contain semantic composition functions.

    No matter how many mixin classes there are covering different kinds of composition functions,
    the `SemanticComposition` class can inherit from all of them and serve as the one-stop shop for performing composition.

    All functions from the base Mixins can be accessed as instance methods on a `SemanticComposition` object.
    """
    def __init__(self, composition_config: Path | str | POGGCompositionConfig):
        """
        Initialize the `SemanticComposition` object

        Each parameter may also be accessed as an instance attribute

        **Parameters / Instance Attributes**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `semantic_algebra` | `SemanticAlgebra` | SemanticAlgebra object that contains functions that perform semantic composition directly |
        """

        self.semantic_algebra = SemanticAlgebra(composition_config)
        self.composition_config = self.semantic_algebra.composition_config



