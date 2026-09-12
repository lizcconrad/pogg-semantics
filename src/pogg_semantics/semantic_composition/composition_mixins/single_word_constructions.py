"""
The `single_word_constructions` module contains the Mixin class for creating SEMENTs that rougly map to one English word, typically containing just one predication.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""

from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

class SingleWordConstructionsMixin:
    """
    The `SingleWordConstructionsMixin` contains functions for creating "starter" SEMENTs
    (typically containing only one predicate and roughly mapping to one English word) from scratch
    """

    @SemCompTracer.trace
    def manual_CARG_synopsis(self, predicate: str, carg_value: str, synopsis_dict: dict,
                        intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        Wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class. Includes a parameter for inserting a manual argument synopsis dict
        if the first result from the SEMI isn't what you want.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT(predicate, carg_value,
                                            intrinsic_variable_properties, synopsis_dict)

    @SemCompTracer.trace
    def manual_synopsis(self, predicate: str, synopsis_dict: dict, intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        Wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class. Includes a parameter for inserting a manual argument synopsis dict
        if the first result from the SEMI isn't what you want.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties, synopsis_dict)

    @SemCompTracer.trace
    def basic(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class. Used in fallback cases where part-of-speech guessing fails.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def adjective(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just an adjective EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def adverb(self, predicate: str, intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        Creates a SEMENT with just an adjective EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def comparative_adjective(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT for a comparative adjective.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        adj = self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)
        comparative = self.semantic_algebra.create_base_SEMENT("more_comp")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(comparative, adj, "ARG1")

    @SemCompTracer.trace
    def superlative_adjective(self, predicate: str, intrinsic_variable_properties: dict = None) -> SEMENT:
        """
        Creates a SEMENT for a comparative adjective.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_tasty_a_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        adj = self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)
        superlative = self.semantic_algebra.create_base_SEMENT("superl")
        return self.semantic_algebra.op_non_scopal_argument_hook_slots(superlative, adj, "ARG1")

    @SemCompTracer.trace
    def conjunction(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def determiner(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a determiner EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_the_q` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'IND': '+'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def holiday(self, name: str, intrinsic_variable_properties: dict = None) -> SEMENT:
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        # set or overwrite QUANT feature to be udef_q
        intrinsic_variable_properties['QUANT'] = "udef_q"

        return self.semantic_algebra.create_CARG_SEMENT("holiday", name, intrinsic_variable_properties)

    @SemCompTracer.trace
    def non_unique_name(self, name: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Name that can be singular or plural and can be quantified with "the" or "a" ... e.g. car names
        "I have a Honda Civic"

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

        # set or overwrite QUANT feature to be def_udef_a_q to allow "a Honda Civic"
        intrinsic_variable_properties['QUANT'] = "def_udef_a_q"

        return self.semantic_algebra.create_CARG_SEMENT("named", name, intrinsic_variable_properties)

    @SemCompTracer.trace
    def name(self, name: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        return self.semantic_algebra.create_CARG_SEMENT("named", name, intrinsic_variable_properties)

    @SemCompTracer.trace
    def plural_name(self, name: str, intrinsic_variable_properties: dict = None) -> SEMENT:
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        # set or overwrite NUM to be pl ...
        # technically this isn't necessary if the name appears "on its own"
        # but if it's the nonhead of a compound that fxn will insert "sg" if the property is not set
        intrinsic_variable_properties['NUM'] = "pl"

        # # set or overwrite QUANT feature to be explicit_or_proper_q
        # intrinsic_variable_properties['QUANT'] = "explicit_or_proper_q"

        return self.semantic_algebra.create_CARG_SEMENT("named_pl", name, intrinsic_variable_properties)

    # @SemCompTracer.trace
    # def the_name(self, name: str, intrinsic_variable_properties: dict = None) -> SEMENT:
    #     # e.g. The Beatles
    #     if intrinsic_variable_properties is None:
    #         intrinsic_variable_properties = {}
    #
    #     # set or overwrite QUANT feature to be proper_q and enforce singular if no value is set
    #     intrinsic_variable_properties['QUANT'] = "_the_q"
    #     if "NUM" not in intrinsic_variable_properties:
    #         intrinsic_variable_properties['NUM'] = "sg"
    #
    #     # TODO: named_n is probably better for things like The Netherlands ... but
    #     return self.semantic_algebra.create_CARG_SEMENT("named", name, intrinsic_variable_properties)

    @SemCompTracer.trace
    def noun(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a noun EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def number(self, digit: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a number EP in it.
        This is a wrapper around `create_CARG_SEMENT` from the `SemanticAlgebra` class,
        but only asks for the value of CARG and assumes the predicate is "card" since it's a number

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `digit` | `str` |  | The digit of the number (i.e. NOT the number spelled out) | `3` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        # TODO: needs support for more than 1-9
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT("card", digit, intrinsic_variable_properties)

    @SemCompTracer.trace
    def preposition(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a preposition EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_in_p_loc` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'MOOD': 'indicative'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def pronoun(self, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT for a pronoun.
        If values for PER and NUM (and GEND for third person) are not specified in the intrinsic_variable_properties dictionary,
        it will be ambiguous between all values.

        ```{info} Possible variables and values for a pronoun's intrinsic variable
        :collapsible:
        | Variable | Values |
        | -------- | ------ |
        | `'PERS'` | `'1'`, `'2'`, `'3'` |
        | `'NUM'` | `'sg'`, `'pl'` |
        | `'GEND'` | `'m'`, `'f'`, `'n'` |
        ```

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `intrinsic_variable_properties` | `dict` of `str:str` | `None` | optional dictionary of properties of the intrinsic variable | `{'PER': '3', 'NUM': 'sg', 'GEND': 'f'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        pron_EP = self.semantic_algebra.create_base_SEMENT("pron", intrinsic_variable_properties)
        pronoun_q_EP = self.determiner("pronoun_q")

        # scopal composition between pronoun quantifier and the pron EP
        return self.semantic_algebra.op_scopal_quantifier(pronoun_q_EP, pron_EP)

    @SemCompTracer.trace
    def quantifier(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a quantifier EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_eat_v_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'TENSE': 'pres'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

    @SemCompTracer.trace
    def unknown_noun(self, word: str, intrinsic_variable_properties: dict=None, synopsis_dict: dict=None) -> SEMENT:
        # if no synopsis dict is provided, assume only ARG0 of type x
        if synopsis_dict is None or synopsis_dict == {}:
            synopsis_dict = {
                "roles": [
                    {
                        "name": "ARG0",
                        "value": "x"
                    }
                ]
            }

        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        if "IND" not in intrinsic_variable_properties:
            intrinsic_variable_properties["IND"] = "+"

        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT("unk_n", word, intrinsic_variable_properties, synopsis_dict)

    @SemCompTracer.trace
    def unknown_adjective(self, word: str, intrinsic_variable_properties: dict = None, synopsis_dict: dict = None) -> SEMENT:
        # if no synopsis dict is provided, assume only ARG0 of type x
        if synopsis_dict is None or synopsis_dict == {}:
            synopsis_dict = {
                "roles": [
                    {
                        "name": "ARG0",
                        "value": "e"
                    },
                    {
                        "name": "ARG1",
                        "value": "x"
                    }
                ]
            }

        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_CARG_SEMENT("unk_a", word, intrinsic_variable_properties, synopsis_dict)

    @SemCompTracer.trace
    def verb(self, predicate: str, intrinsic_variable_properties: dict=None) -> SEMENT:
        """
        Creates a SEMENT with just a verb EP in it.
        This is just a wrapper around `create_base_SEMENT` from the `SemanticAlgebra` class, but is more transparently named for users.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` |  | ERG predicate label | `_eat_v_1` |
        | `intrinsic_variable_properties` | `dict` of `str:str` | None  | optional dictionary of properties of the intrinsic variable | `{'TENSE': 'pres'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}
        return self.semantic_algebra.create_base_SEMENT(predicate, intrinsic_variable_properties)

