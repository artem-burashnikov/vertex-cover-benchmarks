from pathlib import Path

import networkx as nx
import pytest

import algorithms

# Path to datasets directory containing text files.
DATASET_PATH = Path("datasets")


def load_graph(file_path: Path):
    g = nx.read_edgelist(file_path, comments="#")
    g.remove_edges_from(nx.selfloop_edges(g))
    return g


dataset_files = [p for p in DATASET_PATH.iterdir() if p.suffix == ".txt"]


@pytest.mark.parametrize("dataset_file", dataset_files)
@pytest.mark.parametrize(
    "algo_name, algo",
    [
        ("greedy_mvc_nx", algorithms.greedy_mvc_nx),
        ("greedy_mvc", algorithms.greedy_mvc),
        ("edmonds_nx", algorithms.edmonds_nx),
        ("approx2_nx", algorithms.approx2_nx),
        ("mtm", algorithms.mtm),
    ],
)
def test_vertex_cover(dataset_file, algo_name, algo):
    """Check that a given algorithm returns a set cover."""
    graph = load_graph(dataset_file)

    graph_copy = graph.copy()
    _, result, _ = algo(graph_copy)

    fail_message = f"{algo_name} has not covered all edges."
    assert algorithms.is_vertex_cover(graph, result), fail_message
