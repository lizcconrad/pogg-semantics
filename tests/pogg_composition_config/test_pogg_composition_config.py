import os
import pytest
import delphin
from pogg_semantics.pogg_config import _VarIterator, _VarLabeler, POGGCompositionConfig


class Test_VarIterator:
    """
    Tests the VarIterator class.
    """

    @staticmethod
    def test__VarIterator_object(var_iterator):
        # assert whether var_iterator object is of the correct type
        assert isinstance(var_iterator, _VarIterator), "object not of type VarIterator"

    @staticmethod
    def test__VarIterator_iter(var_iterator):
        # assert whether __iter__ returns the VarIterator object
        assert isinstance(var_iterator.__iter__(), _VarIterator), "object not of type VarIterator"

    @staticmethod
    def test__VarIterator_next(var_iterator):
        # assert that the increment occurred correctly
        assert next(var_iterator) == 1

    @staticmethod
    def test__VarIterator_set(var_iterator):
        # assert that the iterator's new value is set correctly
        var_iterator.set(2)
        assert var_iterator.count == 2

    @staticmethod
    def test__VarIterator_reset(var_iterator):
        # assert that the iterator was reset
        var_iterator.set(5)
        var_iterator.reset()
        assert var_iterator.count == 0


class TestVarLabeler:
    """
    Tests the VarLabeler class.
    """
    @staticmethod
    def test__VarLabeler_object(var_labeler):
        # assert whether var_iterator object is of the correct type
        assert isinstance(var_labeler, _VarLabeler), "object not of type VarLabeler"

    @staticmethod
    def test__VarLabeler_next_variable(var_labeler):
        # assert that the labeler produces the correct next variable name
        assert var_labeler.get_var_name("x") == "x1"

    @staticmethod
    def test__VarLabeler_multiple(var_labeler):
        # increment the labeler multiple times and check each one
        for i in range(1, 11):
            assert var_labeler.get_var_name("x") == "x" + str(i)

    @staticmethod
    def test__VarLabeler_reset(var_labeler):
        # increment the labeler a few times
        for i in range(1, 4):
            assert var_labeler.get_var_name("x") == "x" + str(i)

        # reset and check that it was reset correctly
        var_labeler.reset_labeler()
        assert var_labeler.get_var_name("x") == "x1"


class TestPOGGCompositionConfig:
    """
    Tests the POGGCompositionConfig class.
    """
    ### OBJECT INITIALIZATION TESTS ###
    @staticmethod
    def test_POGGCompositionConfig_grammar_location(temp_grammar, pogg_config_mock):
        # assert whether grammar_location matches the provided location
        assert pogg_config_mock.grammar_location == temp_grammar, f"""
                        POGGCompositionConfig object's 'grammar_location' attribute does not match provided location:
                         POGGCompositionConfig object (config.grammar_location): {pogg_config_mock.grammar_location}
                         Provided location (temp_grammar): {temp_grammar}"""


    @staticmethod
    def test_POGGCompositionConfig_SEMI_location(temp_semi, pogg_config_mock):
        # assert whether SEMI_location matches the provided config
        assert pogg_config_mock.SEMI_location == temp_semi, f"""
                                POGGCompositionConfig object's 'SEMI_location' attribute does not match provided location:
                                 POGGCompositionConfig object (config.SEMI_location): {pogg_config_mock.SEMI_location}
                                 Provided location (temp_SEMI): {temp_semi}"""

    @staticmethod
    def test_POGGCompositionConfig_SEMI_object(pogg_config_mock):
        # assert whether SEMI_location matches the provided config
        assert isinstance(pogg_config_mock.SEMI, delphin.semi.SemI), "POGGCompositionConfig object's SEMI is not of type delphin.semi.SemI"

    @staticmethod
    def test_POGGCompositionConfig_VarLabeler_object(pogg_config_mock):
        # assert whether SEMI_location matches the provided config
        assert isinstance(pogg_config_mock.var_labeler, _VarLabeler), "POGGCompositionConfig object's VarLabeler is not of type VarLabeler"


    # test whether exceptions are raised appropriately
    @staticmethod
    def test_POGGCompositionConfig_missing_grammar_location(config_without_grammar):
        with pytest.raises(KeyError):
            POGGCompositionConfig(config_without_grammar)

    @staticmethod
    def test_POGGCompositionConfig_missing_SEMI(config_without_SEMI):
        with pytest.raises(KeyError):
            POGGCompositionConfig(config_without_SEMI)



    ### OBJECT FUNCTION TESTS ###
    @staticmethod
    def test_POGGCompositionConfig_concretize(pogg_config):
        # reset to 0
        pogg_config.var_labeler.reset_labeler()

        #  _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].
        # result of pogg_config.concretize("_give_v_1") should match golden_args
        golden_args = {"ARG0": "e1", "ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}

        assert golden_args == pogg_config.concretize("_give_v_1")

    @staticmethod
    def test_POGGCompositionConfig_concretize_manual_sybopsis(pogg_config):
        # reset to 0
        pogg_config.var_labeler.reset_labeler()

        #  neg : ARG0 i, ARG1 2
        # result of pogg_config.concretize("neg", synopsis_dict) should match golden_args
        golden_args = {"ARG0": "i1", "ARG1": "h2" }

        synopsis_dict = {
            "roles": [
                {"name": "ARG0", "value": "i"},
                {"name": "ARG1", "value": "h"},
            ]
        }

        assert golden_args == pogg_config.concretize("neg", synopsis_dict)


    @staticmethod
    def test_POGGCompositionConfig_concretize_no_synopsis(pogg_config):
        # assert that KeyError is raised when the provided config file doesn't have grammar_location as a key
        with pytest.raises(KeyError) as e:
            pogg_config.concretize("not_a_real_predicate_label")

