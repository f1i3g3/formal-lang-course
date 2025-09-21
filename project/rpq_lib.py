import itertools
from collections.abc import Iterable
from typing import Optional

from networkx import MultiDiGraph
from pyformlang.finite_automaton import Symbol, NondeterministicFiniteAutomaton, State
from scipy.sparse import csc_matrix, kron

from project.graph_lib import graph_to_nfa, regex_to_dfa


# TODO: rewrite code!!


class AdjacencyMatrixFA:
    """
    A finite automaton representation using sparse adjacency matrices.
    """

    def __init__(self, automaton: Optional[NondeterministicFiniteAutomaton]):
        self.start_states = set()
        self.final_states = set()

        if automaton is None:
            self.states_count = 0
            self.adj_matrices = {}
            self.states_to_indexes = {}  # TODO: ?????
            return

        self.states_count = len(automaton.states)
        self.states_to_indexes: dict[State, int] = {
            state: i for i, state in enumerate(automaton.states)
        }
        self.start_states: set[State] = automaton.start_states
        self.final_states: set[State] = automaton.final_states
        self.adj_matrices: dict[Symbol, csc_matrix] = {}

        for from_st in self.states_to_indexes.keys():
            from_idx = self.states_to_indexes[from_st]
            transitions: dict[Symbol, State | set[State]] = automaton.to_dict().get(
                from_st
            )

            if transitions is None:
                continue

            for symbol in transitions.keys():
                if symbol not in self.adj_matrices:
                    self.adj_matrices[symbol] = csc_matrix(
                        (self.states_count, self.states_count), dtype=bool
                    )

                if isinstance(transitions[symbol], Iterable):
                    for to_st in transitions[symbol]:
                        to_idx = self.states_to_indexes[to_st]
                        self.adj_matrices[symbol][from_idx, to_idx] = True
                else:
                    to_st: State = transitions[symbol]
                    to_idx = self.states_to_indexes[to_st]
                    self.adj_matrices[symbol][from_idx, to_idx] = True
        return

    def transitive_closure(self) -> csc_matrix:
        res = csc_matrix((self.states_count, self.states_count), dtype=bool)
        res.setdiag(True)

        for matrix in self.adj_matrices.values():
            res += matrix

        res.astype(bool)
        changed = True

        while changed:
            new_res = (res @ res).astype(bool)

            if (new_res != res).nnz == 0:
                changed = False
            else:
                res = new_res
        return res

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """
        Check if the automaton accepts a given word.
        """
        curr_cfgs: set[State] = self.start_states

        for symbol in word:
            if symbol not in self.adj_matrices:
                return False

            next_configs = set()
            transition_matrix = self.adj_matrices[symbol]

            for curr_state in curr_cfgs:
                for state in self.states_to_indexes.keys():
                    if transition_matrix[
                        self.states_to_indexes[curr_state],
                        self.states_to_indexes[state],
                    ]:
                        next_configs.add(state)

            curr_cfgs = next_configs

        return any(final_st in curr_cfgs for final_st in self.final_states)

    def is_empty(self) -> bool:
        """
        Check if the language recognized by the automaton is empty.
        """
        transitive_closure = self.transitive_closure()

        if transitive_closure is None:
            return True

        for start_st, final_st in itertools.product(
            self.start_states, self.final_states
        ):
            if transitive_closure[
                self.states_to_indexes[start_st], self.states_to_indexes[final_st]
            ]:
                return False

        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    """
    Compute the intersection of two finite automata using tensor product.
    """
    res = AdjacencyMatrixFA(None)
    matrix1, matrix2 = automaton1.adj_matrices, automaton2.adj_matrices

    res.states_count = automaton1.states_count * automaton2.states_count
    symbols = set(matrix1.keys()) & set(matrix2.keys())
    res.adj_matrices = {s: kron(matrix1[s], matrix2[s], format="csc") for s in symbols}

    for st1, st2 in itertools.product(
        automaton1.states_to_indexes.keys(), automaton2.states_to_indexes.keys()
    ):
        idx1, idx2 = (
            automaton1.states_to_indexes[st1],
            automaton2.states_to_indexes[st2],
        )
        res_idx = idx1 * automaton2.states_count + idx2

        res.states_to_indexes[State((st1, st2))] = res_idx
        if st1 in automaton1.start_states and st2 in automaton2.start_states:
            res.start_states.add(State((st1, st2)))
        if st1 in automaton1.final_states and st2 in automaton2.final_states:
            res.final_states.add(State((st1, st2)))
    return res


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    """
    Perform regular path querying on a graph using tensor-based automata intersection.
    """
    regex_dfa_adj_matrix = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_nfa_adj_matrix = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )

    intersection_automaton = intersect_automata(
        regex_dfa_adj_matrix, graph_nfa_adj_matrix
    )
    result_matrix = intersection_automaton.transitive_closure()

    valid_pairs = set()

    for start_state in intersection_automaton.start_states:
        for final_state in intersection_automaton.final_states:
            if result_matrix[
                intersection_automaton.states_to_indexes[start_state],
                intersection_automaton.states_to_indexes[final_state],
            ]:
                start = start_state.value[1].value
                final = final_state.value[1].value

                valid_pairs.add((start, final))

    return valid_pairs
