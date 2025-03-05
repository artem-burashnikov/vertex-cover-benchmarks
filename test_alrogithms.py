from pathlib import Path

import networkx as nx
import pytest
from scipy.io import mmread

import algorithms

# Path to datasets directory containing datasets.
DATASET_PATH = Path("datasets")


def load_graph_from_txt(file_path: Path):
    return nx.read_edgelist(file_path, comments="#")


# Load matrix market dataset into a memory.
def load_graph_from_mtx(file_path: Path):
    return nx.Graph(mmread(file_path))


dataset_files = [
    p for p in DATASET_PATH.iterdir() if p.suffix == ".txt" or p.suffix == ".mtx"
]


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
def test_vertex_cover(dataset_file: Path, algo_name, algo):
    """Check that a given algorithm returns a set cover."""
    graph = (
        load_graph_from_txt(dataset_file)
        if dataset_file.suffix == ".txt"
        else load_graph_from_mtx(dataset_file)
    )

    graph.remove_edges_from(nx.selfloop_edges(graph))

    graph_copy = graph.copy()
    _, result, _ = algo(graph_copy)

    fail_message = f"{algo_name} has not covered all edges."
    assert algorithms.is_vertex_cover(graph, result), fail_message
