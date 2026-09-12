"""
The `sement_util` module contains the `SEMENTUtil` class which has a number of static functions that are useful for
manipulating, comparing, and printing SEMENT structures.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SEMENTUtil_usage.ipynb)
"""
import re

from delphin import mrs

import pogg_semantics.my_delphin.sementcodecs as sementcodecs
from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.my_delphin import is_isomorphic_ignore_predicate_labels

import tabulate
import copy


class SEMENTProcessing:
    """Provides static functions for processing SEMENT structures after they're built.
    Typically for specifying the SEMENT further (e.g. restricting all x-type variables to NUM:sg)
    """

    @staticmethod
    def restrict_x_to_singular(sement: SEMENT):
        for var in sement.variables:
            if var.startswith("x"):
                if "NUM" not in sement.variables[var]:
                    sement.variables[var]["NUM"] = "sg"
        return sement

    @staticmethod
    def restrict_e_to_present(sement: SEMENT):
        for var in sement.variables:
            if var.startswith("e"):
                if "TENSE" in sement.variables[var] and sement.variables[var]["TENSE"] == "tensed":
                    sement.variables[var]["TENSE"] = "pres"
        return sement

    @staticmethod
    def restrict_quant_to_the(sement: SEMENT):
        for rel in sement.rels:
            if rel.predicate == "def_udef_a_q":
                rel.predicate = "_the_q"
        return sement
