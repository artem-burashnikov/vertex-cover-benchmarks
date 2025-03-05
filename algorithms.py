import itertools
import time
from collections import defaultdict

import networkx as nx


# Timer wrapper fo measuring a CPU time of a function execution.
def timer(f):
    def wrapper(*args, **kwargs):
        start = time.process_time()
        res = f(*args, **kwargs)
        finish = time.process_time()
        return (finish - start), res, f.__name__

    return wrapper


def is_vertex_cover(graph: nx.Graph, cover: set) -> bool:
    # Check if edge is covered
    for u, v in graph.edges():
        if u not in cover and v not in cover:
            # Found an edge that is not covered
            return False

    # All edges are covered
    return True


@timer
def greedy_mvc_nx(g):
    """MVC approximation by max degree using NetworkX methods and properties."""
    vertex_cover = set()

    # Untill there are no edges left.
    while g.number_of_edges() > 0:
        # Get vertex with a max degree.
        max_degree_vertex = max(g.degree, key=lambda x: x[1])[0]

        # Remove this vertex and all adjacent edges from a graph.
        g.remove_node(max_degree_vertex)

        # Add this vertex to a cover.
        vertex_cover.add(max_degree_vertex)

    return vertex_cover


@timer
def greedy_mvc(g: nx.Graph):
    """Pavel Anosov's greedy MVC approximation algorithm."""
    vertex_cover = set()

    graph = defaultdict(list, nx.to_dict_of_lists(g))

    while any(graph[node] for node in graph):
        max_key = max(graph.items(), key=lambda x: len(x[1]))[0]
        for neighbour in graph[max_key]:
            graph[neighbour].remove(max_key)
        del graph[max_key]
        vertex_cover.add(max_key)

    return vertex_cover


@timer
def edmonds_nx(g):
    """MVC approximation by NetworkX Edmonds max matching algorithm."""
    vertex_cover = set()
    max_matching = nx.max_weight_matching(g, maxcardinality=True)
    for u, v in max_matching:
        vertex_cover.add(u)
        vertex_cover.add(v)

    return vertex_cover


@timer
def approx2_nx(g):
    """MVC approximation by greedy max matching using NetworkX algorithm."""
    return nx.approximation.min_weighted_vertex_cover(g)


@timer
def mtm(g: nx.Graph):
    """Min-to-Min MVC approximation algorithm."""
    vertex_cover = set()

    while g.number_of_edges() > 0:
        # Find a vertex with minimal degree
        min_degree_vertex, d = min(g.degree, key=lambda x: x[1])

        # If it's an unconnected node, remove it.
        while d == 0:
            g.remove_node(min_degree_vertex)
            # If graph has no nodes left, we are done.
            if g.number_of_nodes() == 0:
                return vertex_cover
            min_degree_vertex, d = min(g.degree, key=lambda x: x[1])

        # Look at the min_degree_vertex neighbors.
        neighbors = list(g.neighbors(min_degree_vertex))

        # If it doesn't have any then remove it from nodes and continue.
        if not neighbors:
            g.remove_node(min_degree_vertex)
            continue

        # Out of all neighbors look for one that has minimal degree.
        min_degree_neighbor, d = min(g.degree(neighbors), key=lambda x: x[1])

        while d == 0:
            g.remove_node(min_degree_neighbor)
            neighbors.remove(min_degree_neighbor)
            if not neighbors:
                break
            min_degree_neighbor, d = min(g.degree(neighbors), key=lambda x: x[1])

        # Add it to vertex cover
        if min_degree_neighbor is not None:
            vertex_cover.add(min_degree_neighbor)
            # Remove it from the graph.
            g.remove_node(min_degree_neighbor)

    return vertex_cover


def brute_force_mvc(graph: nx.Graph):
    """Exponential brute force MVC algorithm."""
    nodes = list(graph.nodes)

    for r in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            if is_vertex_cover(graph, set(subset)):
                return set(subset)

    return set()
