import pytest
import networkx as nx
from pathlib import Path
import algorithms

# Путь к тестовым датасетам
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
    """Проверяет, что алгоритмы действительно возвращают вершинное покрытие."""
    graph = load_graph(dataset_file)

    # Копируем граф перед тестом, чтобы алгоритмы его не изменяли
    graph_copy = graph.copy()
    _, result, _ = algo(graph_copy)

    # Проверяем, является ли результат вершинным покрытием
    assert algorithms.isVertexCover(graph, result), f"{algo_name} не покрыл все рёбра!"
