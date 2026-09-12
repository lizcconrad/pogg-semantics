import os
from glob import glob
import pytest
from pytest_cases import fixture


from pogg_semantics.pogg_config import POGGCompositionConfig
from pogg_semantics.my_delphin import SEMENT, sementcodecs


# get each _fixtures.py file and convert the name to a module path to be put in pytest_plugins
def _as_module(fixture_path: str) -> str:
    path_pieces = fixture_path.split("/")
    module_path = f"tests.{".".join(path_pieces[1:])}"
    # return without .py, i.e. slice off the last 3 characters
    return module_path[:-3]

pytest_plugins = [
    _as_module(fixture) for fixture in glob("./*/*fixtures.py")
]



def pytest_addoption(parser):
    parser.addoption("--test_data_dir", action="store", default="directory that stores data used during testing")
    parser.addoption("--grammar_path", action="store", default="path to compiled grammar")
    parser.addoption("--semi_path", action="store", default="path to SEMI")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    if 'test_data_dir' in metafunc.fixturenames:
        metafunc.parametrize("test_data_dir", [metafunc.config.getoption("test_data_dir")], scope="session")
    if 'grammar_path' in metafunc.fixturenames:
        metafunc.parametrize("grammar_path", [metafunc.config.getoption("grammar_path")], scope="session")
    if 'semi_path' in metafunc.fixturenames:
        metafunc.parametrize("semi_path", [metafunc.config.getoption("semi_path")], scope="session")



# create a temporary POGGConfig YAML file for any tests that need it
@fixture(scope="module")
def pogg_config_file(tmp_path_factory, grammar_path, semi_path):
    tmp_dir = tmp_path_factory.mktemp("pogg_config")

    with open(os.path.join(tmp_dir, "pogg_config.yml"), "w") as config_file:
        config_file.write(f"grammar_location: {grammar_path}\n")
        config_file.write(f"SEMI: {semi_path}")

    yield os.path.join(tmp_dir, "pogg_config.yml")


@fixture(scope="module")
def module_pogg_config(pogg_config_file):
    return POGGCompositionConfig(pogg_config_file)
