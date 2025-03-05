import datetime
from pathlib import Path

import networkx as nx

import algorithms

BENCH_TIMES = 50


# Load dataset into a memory.
def load_data(file_path: Path):
    print(f"Loading dataset {file_path.name}")
    g = nx.read_edgelist(file_path, comments="#")
    print("Dataset has been loaded.")

    return g


# Benchmarking loop. Runs count times.
def bench(algos, graph, count, data_name: Path):
    # For all algorithms...
    for algo_name, algo in algos.items():
        file_path = Path.cwd() / f"{algo_name}_benchmarks-{data_name.name}"

        print(f"Running benchmark of {algo_name}")

        # Write the bench data in file
        with open(file_path, "a") as file:
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
        p for p in Path(Path.cwd() / "datasets").iterdir() if p.suffix == ".txt"
    ]

    # All algorithms to be benched.
    algorithms = {
        "edmonds_nx": algorithms.edmonds_nx,
        "greedy_mvc_nx": algorithms.greedy_mvc_nx,
        "approx2_nx": algorithms.approx2_nx,
        "greedy": algorithms.greedy_mvc,
        "mtm": algorithms.mtm,
    }

    # Run benchmarks.
    for data in datasets:
        graph = load_data(data)
        # Remove selfloops.
        graph.remove_edges_from(nx.selfloop_edges(graph))
        bench(algorithms, graph, BENCH_TIMES, data)
