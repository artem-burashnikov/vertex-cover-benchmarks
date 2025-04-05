import datetime
from pathlib import Path

import networkx as nx
from scipy.io import mmread

import algorithms

BENCH_TIMES = 50

BRUTE_FORCE = "naiveBruteForce"


# Load matrix market dataset into a memory.
def load_mtx_data(file_path: Path):
    print(f"Loading dataset {file_path.name}")
    g = nx.Graph(mmread(file_path))
    print("Dataset has been loaded.")
    return g


# Load textual dataset into a memory.
def load_text_data(file_path: Path):
    print(f"Loading dataset {file_path.name}")
    g = nx.read_edgelist(file_path, comments="#")
    print("Dataset has been loaded.")
    return g


# Benchmarking loop. Runs count times.
def bench(algos, graph: nx.Graph, count, data_name: Path):
    # For all algorithms...
    for algo_name, algo in algos.items():
        file_path = Path.cwd() / f"{algo_name}_benchmarks-{data_name.name}"

        if (graph.number_of_nodes() > 30) and (algo_name == BRUTE_FORCE):
            print(f"Skipping brute force on {data_name.name}...")
            continue

        print(f"Running benchmark of {algo_name}")

        # Write the bench data in file
        with open("benchmarks" / file_path, "a") as file:
            file.write(f"{graph.number_of_nodes()},{graph.number_of_edges()}\n")

            for i in range(count):

                print(f"{datetime.datetime.now()}: Round #{i+1}")

                # Copy graph so many runs are possible.
                graph_copy = nx.Graph.copy(graph)

                # Only this call is timed
                elapsed, result, _ = algo(graph_copy)

                # Note the measured time.
                file.write(f"{elapsed:.15f},{len(result)}\n")

        print("Done.")


# Driver code.
if __name__ == "__main__":
    # All datasets.
    datasets = [
        p
        for p in Path(Path.cwd() / "datasets").iterdir()
        if p.suffix == ".txt" or p.suffix == ".mtx"
    ]

    # All algorithms to be benched.
    algorithms = {
        "edmonds": algorithms.edmonds_nx,
        # "greedy_mvc_nx": algorithms.greedy_mvc_nx,
        "greedy2": algorithms.approx2_nx,
        "greedyPavel": algorithms.greedy_mvc,
        "mtm": algorithms.mtm,
        BRUTE_FORCE: algorithms.brute_force_mvc
    }

    # Run benchmarks on real graphs.
    for data in datasets:
        graph = load_text_data(data) if data.suffix == ".txt" else load_mtx_data(data)
        # Remove selfloops.
        graph.remove_edges_from(nx.selfloop_edges(graph))
        bench(algorithms, graph, BENCH_TIMES, data)
