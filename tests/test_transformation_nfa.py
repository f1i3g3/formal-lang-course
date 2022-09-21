from project.transformation_lib import *

import pytest
import networkx


def test_nonexistent_start():
    graph = networkx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")
    with pytest.raises(Exception, match=".* start .*"):
        graph_to_nfa(graph, {42}, {0})
    with pytest.raises(Exception, match=".* final .*"):
        graph_to_nfa(graph, {0}, {42})


def test_ended_by_zero():
    graph = networkx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")
    nfa = graph_to_nfa(graph, {0}, {1})
    assert nfa.is_equivalent_to(regex_str_to_dfa("(0|1)* 0"))
    for i in range(0, 42, 2):
        assert nfa.accepts("{0:b}".format(i))
        assert not nfa.accepts("{0:b}".format(i + 1))


def test_binary_ended_by_banana_ananas():
    graph = networkx.MultiDiGraph()
    for i in range(ord("a"), ord("z") + 1):
        graph.add_edge(0, 0, label=chr(i))
    graph.add_edge(0, 0, label=" ")
    graph.add_edge(0, 1, label="b")
    graph.add_edge(0, 2, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 3, label="n")
    graph.add_edge(3, 4, label="a")
    graph.add_edge(4, 5, label="n")
    graph.add_edge(5, 6, label="a")
    graph.add_edge(6, 7, label="s")

    nfa = graph_to_nfa(graph, {0}, {6, 7})

    assert nfa.accepts("banana")
    assert nfa.accepts("ananas")
    assert nfa.accepts("bananas")
    assert not nfa.accepts("apple")
