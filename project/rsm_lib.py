from collections.abc import Iterable
from dataclasses import dataclass

from pyformlang.cfg import CFG
from pyformlang.finite_automaton import (
    EpsilonNFA,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from pyformlang.rsa import RecursiveAutomaton

from project.rpq_lib import AdjacencyMatrixFA


@dataclass
class RsmState:
    """
    An RSM state: a (non-terminal, box-internal state) pair.
    """

    nonterm: Symbol
    state: State

    def __eq__(self, other):
        return (
            isinstance(other, RsmState)
            and self.nonterm == other.nonterm
            and self.state == other.state
        )

    def __hash__(self):
        return hash((self.nonterm, self.state))


def cfg_to_rsm(cfg: CFG) -> RecursiveAutomaton:
    """
    Return the RecursiveAutomaton obtained from the given CFG by reusing its textual representation.
    """
    return RecursiveAutomaton.from_text(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> RecursiveAutomaton:
    """
    Return the RecursiveAutomaton parsed from the given EBNF text.
    """
    return RecursiveAutomaton.from_text(ebnf)


def rsm_to_nfa(rsm: RecursiveAutomaton) -> NondeterministicFiniteAutomaton:
    """
    Return an NFA whose states are (non-terminal, state) pairs of the RSM boxes and whose transitions
    mirror the boxes' DFAs, with start and final states lifted from each box.
    """
    nfa = NondeterministicFiniteAutomaton()

    for nonterm, box in rsm.boxes.items():
        dfa: EpsilonNFA = box.dfa

        for st in dfa.start_states:
            nfa.add_start_state(State((nonterm, st.value)))
        for st in dfa.final_states:
            nfa.add_final_state(State((nonterm, st.value)))

        for from_st in dfa.states:
            transitions: dict[Symbol, State | set[State]] = dfa.to_dict().get(from_st)
            if transitions is None:
                continue

            for symbol in transitions:
                for to_st in (
                    transitions[symbol]
                    if isinstance(transitions[symbol], Iterable)
                    else {transitions[symbol]}
                ):
                    nfa.add_transition(
                        State((nonterm, from_st)), symbol, State((nonterm, to_st))
                    )
    return nfa


def boolean_decompress_rsm(rsm: RecursiveAutomaton) -> AdjacencyMatrixFA:
    """
    Return the adjacency-matrix automaton obtained by flattening the RSM into an NFA via rsm_to_nfa.
    """
    return AdjacencyMatrixFA(rsm_to_nfa(rsm))


def get_rsm_state_edges(
    rsm: RecursiveAutomaton, from_state: RsmState
) -> dict[Symbol, set[RsmState]]:
    """
    Return a mapping label -> set of successor RsmStates for edges leaving `from_state`
     inside its box (empty if the box or state is absent).
    """
    nonterm = from_state.nonterm
    edges = {}
    if rsm.get_box(nonterm) is None:
        return {}

    nonterm_edges = rsm.get_box(nonterm).dfa.to_dict()
    if from_state.state in nonterm_edges.keys():
        for label, to_states in nonterm_edges[from_state.state].items():
            if not isinstance(to_states, Iterable):
                edges.setdefault(label, set()).add(RsmState(nonterm, to_states))
                continue

            for to_state in to_states:
                edges.setdefault(label, set()).add(RsmState(nonterm, to_state))

    return edges
