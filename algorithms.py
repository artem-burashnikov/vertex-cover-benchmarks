import networkx as nx
import time
from collections import defaultdict


# Timer wrapper fo measuring a CPU time of a function execution.
def timer(f):
    def wrapper(*args, **kwargs):
        start = time.process_time()
        res = f(*args, **kwargs)
        finish = time.process_time()
        return (finish - start), res, f.__name__

    return wrapper


# MVC approximation by max degree using NetworkX methods and properties.
@timer
def greedy_mvc_nx(g):
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


# MVC approximation by Anosov Pavel
def greedy_mvc(g):
    # Untimed setup
    graph = defaultdict(list)

    for v1, v2 in g.edges:
        if v1 != v2:
            graph[v1].append(v2)
            graph[v2].append(v1)
        else:
            graph[v1].append(v1)

    nodes = list(graph.keys())

    vertex_cover = []

    @timer
    def clean():

        def _remove_highest_degree_node():
            max_key = max(graph.items(), key=lambda x: len(x[1]))[0]
            for neighbour in graph[max_key]:
                graph[neighbour].remove(max_key)
            del graph[max_key]
            nodes.remove(max_key)
            vertex_cover.append(max_key)

        def _has_edges():
            return any(graph[node] for node in graph)

        while _has_edges():
            _remove_highest_degree_node()

    clean()

    return vertex_cover


# MVC approximation by exact max matching using NetworkX Edmonds algorithm.
@timer
def edmonds_nx(g):
    vertex_cover = set()
    max_matching = nx.max_weight_matching(g, maxcardinality=True)
    for u, v in max_matching:
        vertex_cover.add(u)
        vertex_cover.add(v)

    return vertex_cover


# MVC approximation by greedy max matching using NetworkX algorithm.
@timer
def approx2_nx(g):
    return nx.approximation.min_weighted_vertex_cover(g)