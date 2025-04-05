# Experiments for the Course Project

[![Build status][status-shield]][status-url]
[![BSD-3-Clause License][license-shield]][license-url]

This repository contains code and data for running experiments used in the course project.

## Repository Structure

- `datasets/` — input data used in experiments.
- `algorithms.py` — algorithms for approximation of mvc.
- `main.py` — driver code.
- `stats.py` — script that draws histograms and checks p-values.
- `README.md` — this instruction file.

## How to Reproduce the Experiments

### 1. Install Dependencies

You need git, Python 3.13 and some required libraries.
Install them in an isolated manner using:

```bash
git clone https://github.com/artem-burashnikov/greedy_mvc_benchmarks.git && \
cd greedy_mvc_benchmarks && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt
```
### 3. Running experiments

You should set up your test environment first so that OS doesn't affect the results.

To run experiments execute

```bash
python3 main.py
```

By default, all agorithms will be tested against all datasets.

### 4. Veifying the results

After collectiong benchmark data you can run

```bash
python3 stats.py <bench_results.txt>
```

To check if benchmark data satisfies normal distribution.


## License

The project is licensed under a [BSD-3-Clause License][license-url].

[license-url]: LICENSE
[license-shield]: https://img.shields.io/github/license/artem-burashnikov/greedy_mvc_benchmarks?style=for-the-badge&color=blue
[status-shield]: https://img.shields.io/github/actions/workflow/status/artem-burashnikov/greedy_mvc_benchmarks/.github%2Fworkflows%2Fci.yml?style=for-the-badge
[status-url]: https://github.com/artem-burashnikov/greedy_mvc_benchmarks/blob/main/.github/workflows/ci.yml
