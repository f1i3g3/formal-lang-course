from typing import Set

import cfpq_data
import networkx
from networkx import MultiDiGraph
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


class GraphInformation:
    """
    Class for storing some graph properties.
    """

    nodes: int
    edges: int
    labels: Set[str]

    def __init__(self, nodes, edges, labels):
        self.nodes = nodes
        self.edges = edges
        self.labels = labels

    def __eq__(self, other):
        result = (
            isinstance(other, GraphInformation)
            and self.nodes == other.nodes
            and self.edges == other.edges
            and self.labels == other.labels
        )

        return result


def get_graph_info(graph_name):
    """
    Retrieve GraphInformation by graph's name.
    """
    path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path)

    nodes_num = graph.number_of_nodes()
    edges_num = graph.number_of_edges()
    labels = set(cfpq_data.get_sorted_labels(graph))

    return GraphInformation(nodes_num, edges_num, labels)


def generate_and_write_two_cycles_graph(num_first, num_second, labels, path):
    """
    Create a two-cycle graph with numbers of nodes in cycles and given labels and save it in DOT format by given path.
    """
    graph = cfpq_data.labeled_two_cycles_graph(num_first, num_second, labels=labels)

    networkx.nx_pydot.write_dot(graph, path)


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """

    """
    return Regex(regex).to_epsilon_nfa().minimize()


def graph_to_nfa(
        graph: MultiDiGraph, start_states: Set[int] = None, final_states: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    """

    """
    result_graph = NondeterministicFiniteAutomaton()
    result_graph.add_transitions(
        [(x, l, y) for x, y, l in graph.edges(data="label") if l]
    )

    # TODO: documentation!!

    nodes = graph.nodes()

    if not start_states:
        start_states = nodes
    elif not start_states.issubset(nodes):
        raise Exception(
            f"Error! Initial graph does not contain start states: {start_states.difference(set(nodes))}."
        )

    if not final_states:
        final_states = nodes
    elif not final_states.issubset(nodes):
        raise Exception(
            f"Error! Initial graph does not contain final states: {final_states.difference(set(nodes))}."
        )

    for s in start_states:
        result_graph.add_start_state(s)
    for s in final_states:
        result_graph.add_final_state(s)

    return result_graph
