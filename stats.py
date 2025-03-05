import sys
from pathlib import Path

import matplotlib.pyplot as plt
from scipy import stats


def check_stats(file_path: Path):
    with open(file_path) as file:
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
