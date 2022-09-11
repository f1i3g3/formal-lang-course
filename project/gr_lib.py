import string
import cfpq_data
import networkx


def get_gr_info(gr_name: string):
    gr = cfpq_data.graph_from_csv(cfpq_data.download(gr_name))

    nodes_num = gr.number_of_nodes()
    edges_num = gr.number_of_edges()
    labels = {i[2]["label"] for i in gr.edges.data(default=True)}

    return nodes_num, edges_num, labels


def generate_and_write_two_cycles_graph(n, m, labels, path):
    networkx.drawing.nx_pydot.write_dot(
        cfpq_data.labeled_two_cycles_graph(n, m, labels=labels), path
    )
