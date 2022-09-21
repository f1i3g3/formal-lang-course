from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)

import networkx


def regex_to_nfa(rx):
    return Regex(rx).to_epsilon_nfa().minimize()


def graph_to_dfa(
    initial_graph, start_states: set | None = None, final_states: set | None = None
):
    final_graph = NondeterministicFiniteAutomaton()
    final_graph.add_transitions(
        [x, l, y] for x, y, l in initial_graph.edges(data="label") if l
    )

    nodes = initial_graph.nodes

    if not start_states:
        start_states = nodes
    elif not start_states.issubset(nodes):
        raise Exception("Error!")

    if not final_states_states:
        final_states = nodes
    elif not final_states.issubset(nodes):
        raise Exception("Error!")

    for s in start_states:
        final_states.add_start_state(s)
    for s in final_states:
        final_states.add_finish_state(s)

    return final_states
