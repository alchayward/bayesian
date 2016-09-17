import networkx as nx
from itertools import combinations
from useful import unique_pairs


def add_weights_to_graph(graph, weight_fn):
    g = graph.copy()  # lets keep things functional
    for e in g.edges():
        g[e]['weight'] = weight_fn(e)
    return g


def complete_graph_from_node_list(nodes):
    edges = combinations(nodes, 2)
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


def games_from_weighted_graph(g):
    return unique_pairs(nx.max_weight_matching(g), lambda x, y: x is y)
