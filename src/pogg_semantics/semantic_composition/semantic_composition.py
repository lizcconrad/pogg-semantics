"""
The base_constructions module contains classes that help in creating SEMENTs from scratch as well as performing composition on existing SEMENTs.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""

from pathlib import Path
from pogg.pogg_config import POGGCompositionConfig
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.composition_mixins.single_word_constructions import SingleWordConstructionsMixin
from pogg.semantic_composition.composition_mixins.base_constructions import BaseConstructionsMixin
from pogg.semantic_composition.composition_mixins.heuristic_constructions import HeuristicConstructionsMixin
from pogg.semantic_composition.composition_mixins.boolean_constructions import BooleanConstructionsMixin
# TODO: how can i make these optional?
# data specific mixins
# from pogg.semantic_composition.composition_mixins.perplexity_constructions import PerplexityConstructionsMixin

class SemanticComposition(SingleWordConstructionsMixin,
                          BaseConstructionsMixin,
                          HeuristicConstructionsMixin,
                          BooleanConstructionsMixin):
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



