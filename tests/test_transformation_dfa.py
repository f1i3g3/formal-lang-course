from project.transformation_lib import *

import pytest
import networkx


def test_nonexistent_start():
    initial_graph = networkx.MultiDiGraph()
    initial_graph.add_edge(0, 0, label="1")
    initial_graph.add_edge(0, 1, label="0")
    initial_graph.add_edge(1, 1, label="0")
    initial_graph.add_edge(1, 0, label="1")

    with pytest.raises(Exception, match=".* start .*"):
        graph_to_nfa(initial_graph, {42}, {0})
    with pytest.raises(Exception, match=".* final .*"):
        graph_to_nfa(initial_graph, {0}, {42})


def test_ended_by_zero():
    initial_graph = networkx.MultiDiGraph()
    initial_graph.add_edge(0, 0, label="1")
    initial_graph.add_edge(0, 1, label="0")
    initial_graph.add_edge(1, 1, label="0")
    initial_graph.add_edge(1, 0, label="1")

    final_graph = graph_to_nfa(initial_graph, {0}, {1})

    assert final_graph.is_equivalent_to(regex_to_dfa("(0|1)* 0"))
    for i in range(0, 42, 2):
        assert final_graph.accepts("{0:b}".format(i))
        assert not final_graph.accepts("{0:b}".format(i + 1))


def test_ended_by_banana_ananas():
    initial_graph = networkx.MultiDiGraph()
    for i in range(ord("a"), ord("z") + 1):
        initial_graph.add_edge(0, 0, label=chr(i))
    initial_graph.add_edge(0, 0, label=" ")
    initial_graph.add_edge(0, 1, label="b")
    initial_graph.add_edge(0, 2, label="a")
    initial_graph.add_edge(1, 2, label="a")
    initial_graph.add_edge(2, 3, label="n")
    initial_graph.add_edge(3, 4, label="a")
    initial_graph.add_edge(4, 5, label="n")
    initial_graph.add_edge(5, 6, label="a")
    initial_graph.add_edge(6, 7, label="s")

    final_graph = graph_to_nfa(initial_graph, {0}, {6, 7})

    assert final_graph.accepts("banana")
    assert final_graph.accepts("ananas")
    assert final_graph.accepts(" bananas")
    assert not final_graph.accepts("apple")
