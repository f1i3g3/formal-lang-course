from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)

import networkx


def regex_to_dfa(rx: str) -> DeterministicFiniteAutomaton:
    return Regex(rx).to_epsilon_nfa().minimize()


def graph_to_nfa(
    initial_graph: networkx.MultiDiGraph,
    start_states: set = None,
    final_states: set = None,
) -> NondeterministicFiniteAutomaton:
    final_graph = NondeterministicFiniteAutomaton()
    final_graph.add_transitions(
        [(x, l, y) for x, y, l in initial_graph.edges(data="label") if l]
    )

    nodes = initial_graph.nodes()

    if not start_states:
        start_states = nodes
    elif not start_states.issubset(nodes):
        raise Exception(
            f"Error! Initial graph does not contain start states: {start_states.difference(set(nodes))}"
        )

    if not final_states:
        final_states = nodes
    elif not final_states.issubset(nodes):
        raise Exception(
            f"Error! Initial graph does not contain final states: {final_states.difference(set(nodes))}"
        )

    for s in start_states:
        final_graph.add_start_state(s)
    for s in final_states:
        final_graph.add_final_state(s)

    return final_graph
