import networkx as nx
from pathlib import Path
import algorithms

BENCH_TIMES = 40


# Load dataset into a memory.
def load_data(file_path: Path):
    print(f"Loading dataset {file_path.name}")
    g = nx.read_edgelist(file_path, comments="#")
    print("Dataset has been loaded.")

    return g


# Benchmarking loop. Runs count times.
def bench(algorithms, graph, count):
    # For all algorithms...
    for algo_name, algo in algorithms.items():
        file_path = Path.cwd() / f"{algo_name}_benchmarks"
        print(f"Running benchmark of {algo_name}")
        # Write the bench data in file
        with open(file_path, "a") as file:
            for i in range(count):
                print(f"Round #{i+1}")
                # Copy graph so many runs are possible.
                graph_copy = nx.Graph.copy(graph)
                # Only this call is timed
                elapsed, result, _ = algo(graph_copy)
                # Note the measured time.
                file.write("{:.15f}\n".format(elapsed))
        print(f"Done.")


# Driver code.
if __name__ == "__main__":
    # All datasets.
    datasets = [x.absolute().resolve() for x in Path("datasets/").iterdir()]

    # All algorithms to be benched.
    algorithms = {
        "Edmonds": algorithms.approx_edmonds_nx,
        "Greedy": algorithms.approx_nx,
        "2-approx": algorithms.approx2_nx,
    }

    # Run benchmarks.
    for data in datasets:
        graph = load_data(data)
        bench(algorithms, graph, BENCH_TIMES)
