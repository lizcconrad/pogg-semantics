import os
from pytest_cases import fixture
from tempfile import NamedTemporaryFile
from pogg_semantics.pogg_config import _VarIterator, _VarLabeler, POGGCompositionConfig


@fixture
def var_iterator():
    return _VarIterator()

@fixture
def var_labeler():
    return _VarLabeler()


@fixture(scope="class")
def temp_grammar():
    temp_grammar = NamedTemporaryFile(suffix=".dat")
    yield temp_grammar.name
    temp_grammar.close()


@fixture(scope="class")
def temp_semi():
    temp_semi = NamedTemporaryFile(suffix=".smi")
    yield temp_semi.name
    temp_semi.close()


@fixture(autouse=True, scope="class")
def temp_config(temp_grammar, temp_semi):
    # make temporary files
    temp_config = NamedTemporaryFile(suffix=".yml")

    # write config information
    with open(temp_config.name, "w") as f:
        f.write(f"grammar_location: {temp_grammar}\n")
        f.write(f"SEMI: {temp_semi}\n")

    yield temp_config.name

    temp_config.close()


@fixture(scope="class")
def pogg_config_mock(temp_config):
    # make mock POGGCompositionConfig, for testing object initialization
    return POGGCompositionConfig(temp_config)


@fixture(scope="class")
def pogg_config(pogg_config_file):
    # create a POGGCompositionConfig object that points to a real grammar for testing functionality
    return POGGCompositionConfig(pogg_config_file)


@fixture
def config_without_grammar():
    # create temporary file with missing information
    # make temporary file
    config_without_grammar_file = NamedTemporaryFile(suffix=".yml")
    # write dummy information
    with open(config_without_grammar_file.name, "w") as f:
        f.write("dummy_key: dummy_value\n")

    yield config_without_grammar_file.name

    config_without_grammar_file.close()


@fixture
def config_without_SEMI():
    # create temporary file with missing information
    # make temporary file
    config_without_SEMI_file = NamedTemporaryFile(suffix=".yml")

    # write fake grammar_location so that it passes that check and moves to the SEMI check during test
    with open(config_without_SEMI_file.name, "w") as f:
        f.write("grammar_location: dummy_value\n")

    yield config_without_SEMI_file.name

    config_without_SEMI_file.close()
