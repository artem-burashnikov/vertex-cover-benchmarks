from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path
import sys


def check_stats(file_path: Path):
    with open(file_path, "r") as file:
        t = [float(line.split()[0]) for line in file]

        print(f"NormalTest p-value: {stats.normaltest(t)[1]}")
        print(f"Shapirp p-value: {stats.shapiro(t)[1]}")

        plt.hist(t)
        plt.show()


def usage():
    print("Usage: python3 stats <file_path>")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    file_path = sys.argv[1]
    check_stats(file_path)
