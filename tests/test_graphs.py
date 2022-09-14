import filecmp
import os
import pytest
import networkx

from project.graph_lib import *


def test_get_graph_info():
    actual_info = get_graph_info(True, "people")
    expected_info = GraphInformation(
        377,
        640,
        {
            "allValuesFrom",
            "comment",
            "complementOf",
            "disjointWith",
            "domain",
            "drives",
            "equivalentClass",
            "first",
            "has_pet",
            "intersectionOf",
            "inverseOf",
            "is_pet_of",
            "label",
            "maxCardinality",
            "minCardinality",
            "onProperty",
            "range",
            "reads",
            "rest",
            "service_number",
            "someValuesFrom",
            "subClassOf",
            "subPropertyOf",
            "type",
            "unionOf",
        },
    )

    assert actual_info == expected_info


def test_no_name_graph():
    with pytest.raises(Exception):
        get_graph_info(True, "this_name_surely_does_not_exist")


def test_empty_graph():
    actual_info = get_graph_info(False, networkx.empty_graph())
    expected_info = GraphInformation(0, 0, set())

    assert expected_info == actual_info


def test_trivial_graph():
    actual_info = get_graph_info(False, networkx.trivial_graph())
    expected_info = GraphInformation(1, 0, set())

    assert expected_info == actual_info


def test_generate_two_cycles_graph():
    generate_and_write_two_cycles_graph(3, 2, ["x", "y"], "tests/files/generated.dot")

    assert filecmp.cmp("tests/files/generated.dot", "tests/files/expected.dot")

    os.remove("tests/files/generated.dot")


def test_generate_graph_without_cycles():
    with pytest.raises(Exception):
        generate_and_write_two_cycles_graph(
            0, 0, ("x", "y"), "tests/files/generated.dot"
        )
