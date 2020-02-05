# TinyTable

Empirical tool to find the best file format for caching a particular dataset.

## Installation

Install the current PyPI release:

```bash
pip install tinytable
```

Or install from source:

```bash
pip install git+https://github.com/gregorybchris/tinytable
```

## Basic Usage

```bash
# Run the tinytable command to get file size statistics
tinytable --experiment <experiment-name> run --dataset <path-to-dataset> --trials 3

# Generate charts to visualize the best file format
tinytable --experiment <experiment-name> plot

# Delete experiment data
tinytable --experiment <experiment-name> clean
```

## Advanced Usage

```bash
# Subsample the dataset before serializing
tinytable run -d <path-to-dataset> --sample .5

# Don't write the results to a file, just print them
tinytable -e exp1 run -d data/data.csv --no_write

# Specify the directory to which experiments should be saved
tinytable -e exp1 --experiments_dir <path-to-new-experiments-dir> run -d data/data.csv
```