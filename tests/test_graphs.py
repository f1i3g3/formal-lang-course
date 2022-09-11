import filecmp
import os

from project.gr_lib import *


def test_get_graph_info():
    (nodes, edges, labels) = get_gr_info("people")

    # from: https: // jetbrains - research.github.io / CFPQ_Data / dataset / index.html
    assert nodes == 337
    assert edges == 640
    assert labels == {
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
    }


def test_generate_two_cycles_graph():
    generate_and_write_two_cycles_graph(3, 2, ["x", "y"], "./tests/files/generated.dot")

    assert filecmp.cmp("./tests/files/generated.dot", "./tests/files/expected.dot")
    os.remove("./tests/files/generated.dot")
