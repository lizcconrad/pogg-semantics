"""
This module contains the POGGCompositionConfig class, which stores configuration information such as the location of the grammar used for generation.

[See usage examples here.](project:/usage_nbs/pogg/pogg_config_usage.ipynb)
"""

import warnings
import json
from delphin import semi



class _VarIterator:
    """
    Iterator to help with creating handles, indices, and variables in SEMENTs.

    For example, the `ARG0` of the `_cake_n_1` predicate may have a value of `x1`. The `1` comes from this iterator.
    Every time a new variable is introduced the current value of the iterator is used and the iterator is incremented.
    """
    def __init__(self, start=0):
        """
        **Parameters**
        | Parameter | Type | Default | Description |
        | --------- | ---- | ------- | ----------- |
        | `start` | `int` | `0` | Value to start the iterator |

        **Instance Attributes**
        | Attribute | Type | Description |
        | --------- | ---- | ------------ |
        | `count` | `int` | Current value of the iterator |
        """
        self.count = start

    def __iter__(self):
        """Return the iterator object."""
        return self

    def __next__(self):
        """Increment the iterator by 1."""
        self.count += 1
        return self.count

    def set(self, num):
        """
        Set the value of the iterator.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `num` | `int` | Value to set the iterator to |
        """
        self.count = num

    def reset(self):
        """Reset the iterator to 0."""
        self.count = 0


class _VarLabeler:
    """
    Returns the appropriate label for the next created variable.

    For example, for the intrinsic variable of a noun, the type will be `x` and then the object's variable iterator
    (`self.VarIt`) determines the number following the type.
    """
    def __init__(self):
        """
        Make a `VarIterator` which will increment for each variable made and include the number on the variable name.

        **Instance Attributes**
        | Attribute | Type | Description |
        | --------- | ---- | ------------ |
        | `varIt` | `_VarIterator` | VarIterator for the numbers on the variables |
        """
        self.varIt = _VarIterator()

    def get_var_name(self, var_type):
        """
        Get the next variable name, passing in the type of the variable per the ERG variable type hierarchy.

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `var_type` | `str` | type of the variable |

        ```{info} Possible variable types
        :collapsible:
        | Type | Supertype(s) | Description |
        |------|--------------|-------------|
        | `u`  |              | unspecific |
        | `i`  | `u`          | underspecified between `e` and `x` |
        | `p`  | `u`          | underspecified between `h` and `x` |
        | `e`  | `i`          | eventualities (e.g. intrinsic variable of a verb) |
        | `x`  | `i`, `p`     | instance (e.g. intrinsic variable of a noun) |
        | `h`  | `p`          | handle used for scopal composition |
        ```

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `str` | the next variable name |
        """
        return f"{var_type}{next(self.varIt)}"

    def reset_labeler(self):
        """
        Reset the variable labeler's iterator back to `0`.
        """
        self.varIt.reset()


class POGGCompositionConfig:
    """
    Holds configuration information necessary to create and perform composition with SEMENT objects.
    """
    def __init__(self, config_filepath):
        """
         **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ------------ |
        | `config_filepath` | `str` | path to the JSON file which contains the configuration information |

        :::{example} JSON config example
        :collapsible:
        ```
        {
            "grammar_location": "/Users/lizcconrad/Documents/PhD/POGG/ERG/ERG_2023/erg-2023.dat",
            "SEMI": "/Users/lizcconrad/Documents/PhD/POGG/ERG/ERG_2023/trunk/etc/erg.smi"
        }
        ```
        :::

        Provided the provided YAML config file has the appropriate fields, the instance attributes shown in the below table will be accessible.

        **Instance Attributes**
        | Attribute | Type | Description |
        | --------- | ---- | ------------ |
        | `grammar_location` | `str` | location of the grammar used for generation |
        | `SEMI_location` | `str` | location of the SEM-I (Semantic Interface) |
        | `SEMI` | `delphin.SEMI` | PyDelphin SEM-I object, loaded from SEMI_location |
        | `var_labeler` | `_VarLabeler` |  _VarLabeler object used to provide a label for each new variable in a semantic structure |
        """
        with open(config_filepath, 'r') as config_file:
            json_config = json.load(config_file)

        self.grammar_location = None
        self.SEMI_location = None
        self.SEMI = None
        self.var_labeler = None

        # save grammar_location in the POGGCompositionConfig object
        try:
            self.grammar_location = json_config['grammar_location']
        except KeyError:
            raise KeyError("'grammar_location' is missing in the config file")

        # save SEMI_location in the POGGCompositionConfig object and load the SEMI object
        try:

            self.SEMI_location = json_config['SEMI']
            # suppress SEMI warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.SEMI = semi.load(self.SEMI_location)
        except KeyError:
            raise KeyError("'SEMI' is missing in the config file")

        self.var_labeler = _VarLabeler()

    def concretize(self, predicate, manual_synopsis=None):
        """
        Given a predicate label, find the semantic argument slots and concretize the variable names.

        For example, if according to the SEMI, the variable type of the predicate's `ARG1` is `e`
        then give it a concrete value such as `e1`. Return as a dict of arguments and their concrete variable values.

        Optionally, provide a synopsis dictionary if the synopsis pulled from the SEMI is not the desired version for a predicate label.

        **Parameters**
        | Parameter | Type | Default | Description | Example |
        | --------- | ---- | ------- | ----------- | ------- |
        | `predicate` | `str` | -- | ERG predicate label | `_cookie_n_1` for the word 'cookie' |
        | `manual_synopsis` | `str` | `None` | Dictionary of predicate roles and their variable types | See dropdown |

        ````{example} Synopsis Dictionary Example
        :collapsible:
        A synopsis dictionary is a dictionary with one key, `roles` which contains a list of dictionaries
        detailing the name of each argument and its variable type.

        Because the `find_synopsis` function from PyDelphin only returns the first synopsis for a predicate label,
        it is sometimes necessary to provide the synopsis manually to ensure proper generation.

        Below is an example for the predicate `_cool_a_1` which has two versions, and the second one is required for generating
        phrases like *the cool jacket*.

        ```
        _cool_a_1 : ARG0 e, [ ARG1 u ], [ ARG2 i ].
        _cool_a_1 : ARG0 e, ARG1 i.
        ```

        ```
        {
            "roles": [
                {"name": "ARG0", "value": "e"}
                {"name": "ARG1", "value": "i"}
            ]
        }
        ```

        ````

        **Returns**
        | Type | Description | Example |
        | ---- | ----------- | ------- |
        | dict of `str`:`str` | dict of semantic slots and their variable values | `{'ARG1': 'x1'}` |
        """

        if manual_synopsis is None:
            try:
                synopsis = self.SEMI.find_synopsis(predicate)
                synopsis_dict = synopsis.to_dict()
            except semi.SemIError:
                raise KeyError(f"Couldn't find {predicate} in the SEMI")
        else:
            # TODO: make this so that the user enters in what is in the .smi file rather than a full dictionary structure
            synopsis_dict = manual_synopsis


        args_dict = {}
        for role in synopsis_dict['roles']:
            # currently, role['value'] is just a variable type, like e
            # we still want that in the final variable name, so pass it in as the prefix to the var_labeler
            # but set the value of the role in the args_dict to be the returned var_name (something like e2)
            args_dict[role['name']] = self.var_labeler.get_var_name(role['value'])

        return args_dict
