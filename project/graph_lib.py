import string
from typing import Iterable

import cfpq_data
import networkx
import networkx as nx


class GraphInformation:
    nodes: int
    edges: int
    labels: Iterable[str]

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


def get_graph_info(load_flag: bool, graph_param):
    if load_flag:
        graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_param))
    else:
        graph = graph_param

    nodes_num = graph.number_of_nodes()
    edges_num = graph.number_of_edges()
    labels = {i[2]["label"] for i in graph.edges.data(default=True)}

    return GraphInformation(nodes_num, edges_num, labels)


def generate_and_write_two_cycles_graph(n, m, labels, path):
    networkx.drawing.nx_pydot.write_dot(
        cfpq_data.labeled_two_cycles_graph(n, m, labels=labels), path
    )
